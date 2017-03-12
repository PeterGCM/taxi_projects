import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO, MIN_RATIO_RESIDUAL
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import statsmodels.api as sm
from traceback import format_exc

logger = get_logger()
numWorker = 4
#
year = '20%02d' % 9
# depVar = 'roamingTime'
depVar = 'interTravelTime'
#
#
if_dpath = dpaths[depVar, 'priorPresence']
if_prefixs = prefixs[depVar, 'priorPresence']
of_dpath = dpaths[depVar, 'influenceGraph']
of_prefixs = prefixs[depVar, 'influenceGraph']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(processorNum):
    for i, fn in enumerate(get_all_files(if_dpath, '%s%s*.csv' % (if_prefixs, year))):
        if i % numWorker != processorNum:
            continue
        fpath = '%s/%s' % (if_dpath, fn)
        process_file(fpath)


def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    _, _, _, reducerID = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        ig_fpath = '%s/%s%s.pkl' % (of_dpath, of_prefixs, reducerID)
        count_fpath = '%s/%scount-%s.pkl' % (of_dpath, of_prefixs, reducerID)
        if check_path_exist(ig_fpath):
            return None
        #
        logger.info('Start loading; %s-%s' % (year, reducerID))
        df = pd.read_csv(fpath)
        influenceGraph = {}
        countRelation = {k: 0 for k in ['sigPos', 'sigNeg', 'XsigPos', 'XsigNeg']}
        num_drivers = len(set(df['did']))
        for i, did1 in enumerate(set(df['did'])):
            if i % 10 == 0:
                logger.info('Doing regression %.2f; %s-%s' % (i / float(num_drivers), year, reducerID))
            did1_df = df[(df['did'] == did1)].copy(deep=True)
            numObservations = len(did1_df)
            minDFResiduals = numObservations * MIN_RATIO_RESIDUAL
            did1_df = did1_df.drop(['month', 'day', 'hour', 'zi', 'zj', 'did'], axis=1)
            if '%d' % did1 in did1_df.columns:
                did1_df = did1_df.drop(['%d' % did1], axis=1)
            #
            candi_dummies = []
            num_iter = 1
            while True:
                for i, vs in enumerate(zip(*did1_df.values)):
                    if did1_df.columns[i] == depVar:
                        continue
                    if sum(vs) > numObservations * MIN_PICKUP_RATIO * num_iter:
                        candi_dummies.append(did1_df.columns[i])
                numIndepVariables = len(candi_dummies)
                if numIndepVariables == 0:
                    break
                if numObservations < numIndepVariables + minDFResiduals:
                    candi_dummies = []
                    num_iter += 1
                else:
                    break
            if not candi_dummies:
                continue
            y = did1_df[depVar]
            X = did1_df[candi_dummies]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            for _did0, pv in res.pvalues.iteritems():
                if _did0 == 'const':
                    continue
                coef = res.params[_did0]
                if pv < SIGINIFICANCE_LEVEL:
                    if coef < 0:
                        countRelation['sigNeg'] += 1
                        influenceGraph[int(_did0), did1] = (res.f_pvalue, pv, coef)
                    elif coef > 0:
                        countRelation['sigPos'] += 1
                else:
                    if coef < 0:
                        countRelation['XsigNeg'] += 1
                    elif coef > 0:
                        countRelation['XsigPos'] += 1
        #
        logger.info('Start pickling; %s-%s' % (year, reducerID))
        save_pickle_file(ig_fpath, influenceGraph)
        save_pickle_file(count_fpath, countRelation)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s-%s' % (year, reducerID)), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()
