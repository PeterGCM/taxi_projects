import __init__
#
'''

'''
#
from community_analysis import tfZ_TP_dpath, tfZ_TP_prefix
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


def run(processorNum):
    ir = 'influenceGraph'
    #
    tm = 'spendingTime'
    year = '2009'
    check_dir_create(dpaths[tm, year, ir])
    #
    for i, tfZ_TP_fn in enumerate(get_all_files(tfZ_TP_dpath, '%s%s*.csv' % (tfZ_TP_prefix, year))):
        if i % 3 != processorNum:
            continue
        tfZ_TP_fpath = '%s/%s' % (tfZ_TP_dpath, tfZ_TP_fn)
        process_file(tfZ_TP_fpath)


def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    _, year, reducerID = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        tm = 'spendingTime'
        st_graph_dpath = dpaths[tm, year, 'influenceGraph']
        st_graph_prefix = prefixs[tm, year, 'influenceGraph']
        SP_graph_fpath = '%s/%s%s.pkl' % (st_graph_dpath, st_graph_prefix, reducerID)
        count_fpath = '%s/%scount-%s.pkl' % (st_graph_dpath, st_graph_prefix, reducerID)
        if check_path_exist(SP_graph_fpath):
            return None
        #
        logger.info('Start loading; %s-%s' % (year, reducerID))
        df = pd.read_csv(fpath)
        SP_graph = {}
        SPALL_graph = {k: 0 for k in ['sigPos', 'sigNeg', 'XsigPos', 'XsigNeg']}
        num_drivers = len(set(df['did']))
        for i, did1 in enumerate(set(df['did'])):
            if i % 10 == 0:
                logger.info('Doing regression %.2f; %s-%s' % (i / float(num_drivers), year, reducerID))
            did1_df = df[(df['did'] == did1)].copy(deep=True)
            numObservations = len(did1_df)
            minDFResiduals = numObservations * MIN_RATIO_RESIDUAL
            did1_df = did1_df.drop(['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did'], axis=1)
            if '%d' % did1 in did1_df.columns:
                did1_df = did1_df.drop(['%d' % did1], axis=1)
            #
            candi_dummies = []
            num_iter = 1
            while True:
                for i, vs in enumerate(zip(*did1_df.values)):
                    if did1_df.columns[i] == tm:
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
            y = did1_df[tm]
            X = did1_df[candi_dummies]
            X = sm.add_constant(X)
            SP_res = sm.OLS(y, X, missing='drop').fit()
            for _did0, pv in SP_res.pvalues.iteritems():
                if _did0 == 'const':
                    continue
                coef = SP_res.params[_did0]
                if pv < SIGINIFICANCE_LEVEL:
                    if coef < 0:
                        SPALL_graph['sigNeg'] += 1
                        SP_graph[int(_did0), did1] = (SP_res.f_pvalue, pv, coef)
                    elif coef > 0:
                        SPALL_graph['sigPos'] += 1
                else:
                    if coef < 0:
                        SPALL_graph['XsigNeg'] += 1
                    elif coef > 0:
                        SPALL_graph['XsigPos'] += 1
        #
        logger.info('Start pickling; %s-%s' % (year, reducerID))
        save_pickle_file(SP_graph_fpath, SP_graph)
        save_pickle_file(count_fpath, SPALL_graph)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s-%s' % (year, reducerID)), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()
