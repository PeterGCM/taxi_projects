import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO, MIN_RATIO_RESIDUAL
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import csv
import statsmodels.api as sm
from traceback import format_exc

logger = get_logger()
numWorker = 11
#
year = '20%02d' % 9
depVar = 'roamingTime'
# depVar = 'interTravelTime'
#
#
if_dpath = dpaths[depVar, 'priorPresence']
if_prefixs = prefixs[depVar, 'priorPresence']
of_dpath = dpaths[depVar, 'sigRelation']
of_prefixs = prefixs[depVar, 'sigRelation']
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
    _, _, _, _did1 = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        ofpath = '%s/%s%s-%s.csv' % (of_dpath, of_prefixs, year, _did1)
        if check_path_exist(ofpath):
            return None
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['did',
                      'numObservations', 'numPrevDrivers',
                      'thNumEncounter', 'numIndepVariables',
                      'numSigRelationship', 'sigRelation']
            writer.writerow(header)
        #
        logger.info('Start loading; %s-%s' % (year, _did1))
        df = pd.read_csv(fpath)
        numObservations = len(df)
        minDFResiduals = numObservations * MIN_RATIO_RESIDUAL
        did1_df = df.drop(['month', 'day', 'hour', 'zi', 'zj', 'did'], axis=1)
        if _did1 in did1_df.columns:
            did1_df = did1_df.drop([_did1], axis=1)
        numPrevDrivers = len(did1_df.columns) - 1
        #
        candi_dummies = []
        num_iter = 1
        while True:
            thNumEncounter = numObservations * MIN_PICKUP_RATIO * num_iter
            for i, vs in enumerate(zip(*did1_df.values)):
                if did1_df.columns[i] == depVar:
                    continue
                if sum(vs) > thNumEncounter:
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
            return None
        y = did1_df[depVar]
        X = did1_df[candi_dummies]
        X = sm.add_constant(X)
        res = sm.OLS(y, X, missing='drop').fit()
        sigRelatioin = []
        for _did0, pv in res.pvalues.iteritems():
            if _did0 == 'const':
                continue
            if pv < SIGINIFICANCE_LEVEL:
                sigRelatioin += [_did0]
        with open(ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [_did1,
                       numObservations, numPrevDrivers,
                       thNumEncounter, numIndepVariables,
                       len(sigRelatioin), '&'.join(sigRelatioin)]
            writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s-%s' % (year, _did1)), 'w') as f:
            f.write(format_exc())
        raise


def summary():
    pass


if __name__ == '__main__':
    run(0)
