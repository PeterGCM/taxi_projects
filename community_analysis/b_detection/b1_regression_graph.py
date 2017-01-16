import __init__
#
'''

'''
#
from community_analysis import tfZ_TP_dpath, tfZ_TP_prefix
from community_analysis import SP_graph_dpath, SP_graph_prefix
from community_analysis import RP_graph_dpath, RP_graph_prefix
from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
import numpy as np
import statsmodels.api as sm
from traceback import format_exc

logger = get_logger()


def run():
    for graph_dpath in [RP_graph_dpath, SP_graph_dpath]:
        check_dir_create(graph_dpath)
    #
    init_multiprocessor(3)
    count_num_jobs = 0
    for y in range(9, 10):
        yyyy = '20%02d' % y
        for tfZ_TP_fn in get_all_files(tfZ_TP_dpath, '%s%s*.csv' % (tfZ_TP_prefix, yyyy)):
            tfZ_TP_fpath = '%s/%s' % (tfZ_TP_dpath, tfZ_TP_fn)
            # process_file(tfZ_TP_fpath)
            put_task(process_file, [tfZ_TP_fpath])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(fpath):
    def regression(dv, df):
        oc_dv = 'roamingTime' if dv == 'spendingTime' else 'spendingTime'
        rdf = df.copy(deep=True).drop([oc_dv], axis=1)
        rdf = rdf[~(np.abs(rdf[dv] - rdf[dv].mean()) > (3 * rdf[dv].std()))]
        candi_dummies = []
        num_iter = 1
        while True:
            for i, vs in enumerate(zip(*rdf.values)):
                if rdf.columns[i] == dv:
                    continue
                if sum(vs) > len(rdf) * MIN_PICKUP_RATIO * num_iter:
                    candi_dummies.append(rdf.columns[i])
            if len(rdf) <= len(candi_dummies):
                candi_dummies = []
                num_iter += 1
            else:
                break
        y = rdf[dv]
        X = rdf[candi_dummies]
        X = sm.add_constant(X)
        return sm.OLS(y, X, missing='drop').fit()
    logger.info('Start handling; %s' % fpath)
    _, yyyy, reducerID = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        SP_graph_fpath = '%s/%s%s-%s.pkl' % (SP_graph_dpath, SP_graph_prefix, yyyy, reducerID)
        RP_graph_fpath = '%s/%s%s-%s.pkl' % (RP_graph_dpath, RP_graph_prefix, yyyy, reducerID)
        if check_path_exist(SP_graph_fpath):
            return None
        #
        logger.info('Start loading; %s-%s' % (yyyy, reducerID))
        df = pd.read_csv(fpath)
        SP_graph, RP_graph = {}, {}
        num_drivers = len(set(df['did']))
        for i, did1 in enumerate(set(df['did'])):
            if i % 10 == 0:
                logger.info('Doing regression %.2f; %s-%s' % (i / float(num_drivers), yyyy, reducerID))
            did1_df = df[(df['did'] == did1)].copy(deep=True)
            did1_df = did1_df.drop(['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did'], axis=1)
            if '%d' % did1 in did1_df.columns:
                did1_df = did1_df.drop(['%d' % did1], axis=1)
            #
            SP_res = regression('spendingTime', did1_df)
            if SP_res.f_pvalue < SIGINIFICANCE_LEVEL:
                significant_drivers = set()
                for _did0, pv in SP_res.pvalues.iteritems():
                    if _did0 == 'const':
                        continue
                    if pv < SIGINIFICANCE_LEVEL:
                        significant_drivers.add(_did0)
                positive_ef_drivers = set()
                for _did0, cof in SP_res.params.iteritems():
                    if _did0 == 'const':
                        continue
                    if cof > 0:
                        positive_ef_drivers.add(_did0)
                for _did0 in significant_drivers.difference(positive_ef_drivers):
                    RP_graph[int(_did0), did1] = SP_res.params[_did0]

                # negative_ef_drivers = set()
                # for _did0, cof in SP_res.params.iteritems():
                #     if _did0 == 'const':
                #         continue
                #     if cof < 0:
                #         negative_ef_drivers.add(_did0)
                # for _did0 in significant_drivers.difference(negative_ef_drivers):
                #     SP_graph[int(_did0), did1] = SP_res.params[_did0]
            #
            RP_res = regression('roamingTime', did1_df)
            if RP_res.f_pvalue < SIGINIFICANCE_LEVEL:
                significant_drivers = set()
                for _did0, pv in RP_res.pvalues.iteritems():
                    if _did0 == 'const':
                        continue
                    if pv < SIGINIFICANCE_LEVEL:
                        significant_drivers.add(_did0)
                positive_ef_drivers = set()
                for _did0, cof in RP_res.params.iteritems():
                    if _did0 == 'const':
                        continue
                    if cof > 0:
                        positive_ef_drivers.add(_did0)
                for _did0 in significant_drivers.difference(positive_ef_drivers):
                    RP_graph[int(_did0), did1] = RP_res.params[_did0]
        logger.info('Start pickling; %s-%s' % (yyyy, reducerID))
        save_pickle_file(SP_graph_fpath, SP_graph)
        save_pickle_file(RP_graph_fpath, RP_graph)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s-%s' % (yyyy, reducerID)), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()
