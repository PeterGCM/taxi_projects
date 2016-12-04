import __init__
#
'''

'''
#
from community_analysis import regressionModel_dpath
from community_analysis import causalityGraph_dpath, causalityGraph_prefix
from community_analysis import HOUR1
from community_analysis import SIGINIFICANCE_LEVEL
#
from taxi_common.file_handling_functions import get_all_directories, check_dir_create, check_path_exist, get_all_files, get_fn_only, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import fnmatch
import pandas as pd
import statsmodels.api as sm

logger = get_logger()


def run():
    check_dir_create(causalityGraph_dpath)
    #
    for wc in get_all_directories(regressionModel_dpath):
        causalityGraph_wc_dpath = '%s/%s' % (causalityGraph_dpath, wc)
        check_dir_create(causalityGraph_wc_dpath)
    #
    regressionModel_fpaths = []
    for wc in get_all_directories(regressionModel_dpath):

        if wc != 'fb':
            continue

        regressionModel_wc_dpath = '%s/%s' % (regressionModel_dpath, wc)
        for regressionModel_wc_fn in get_all_files(regressionModel_wc_dpath, '', '.csv'):
            for y in range(9, 10):
                yyyy = '20%02d' % (y)
                if fnmatch.fnmatch(regressionModel_wc_fn, '*-%s-*.csv' % yyyy):
                    regressionModel_fpaths.append('%s/%s' % (regressionModel_wc_dpath, regressionModel_wc_fn))
    #
    init_multiprocessor(6)
    count_num_jobs = 0
    for regressionModel_fpath in regressionModel_fpaths:
        # process_file(regressionModel_fpath)
        put_task(process_file, [regressionModel_fpath])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    #
    # init_multiprocessor(8)
    # count_num_jobs = 0
    # for y in range(9, 10):
    #     yyyy = '20%02d' % (y)

        # process_file(yyyy)


def process_file(regressionModel_fpath):
    from traceback import format_exc
    #
    regressionModel_fn = get_fn_only(regressionModel_fpath)
    try:
        logger.info('Handle %s' % regressionModel_fpath)
        _, wc, yyyy, gn = regressionModel_fn[:-len('.csv')].split('-')
        causalityGraph_wc_dpath = '%s/%s' % (causalityGraph_dpath, wc)
        causalityGraph_fpath = '%s/%s%s-%s-%s.pkl' % \
                               (causalityGraph_wc_dpath, causalityGraph_prefix, wc, yyyy, gn)
        if check_path_exist(causalityGraph_fpath):
            logger.info('Already handled %s' % causalityGraph_fpath)
            return None
        logger.info('Loading %s' % regressionModel_fn)
        df = pd.read_csv(regressionModel_fpath)
        df = df[(df['roamingTime'] <= HOUR1) & (df['roamingTime'] > 0)]
        gn_drivers = set(df['did'])
        logger.info('Start regression %s' % regressionModel_fn)
        causalityGraph = list()
        for did1 in gn_drivers:
            did1_df = df[(df['did'] == did1) & (df['%d' % did1] == 1)].copy(deep=True)
            data_multi_reg = did1_df.drop(['month', 'day', 'timeFrame', 'zi', 'zj', 'groupName', 'did', '%d' % did1], axis=1)
            #
            candi_dummies = []
            for i, vs in enumerate(zip(*data_multi_reg.values)):
                if data_multi_reg.columns[i] == 'roamingTime':
                    continue
                if sum(vs) != 0:
                    candi_dummies.append(data_multi_reg.columns[i])
            if not candi_dummies:
                continue
            y = data_multi_reg['roamingTime']
            X = data_multi_reg[candi_dummies]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            #
            significant_drivers = set()
            for _did0, pv in res.pvalues.iteritems():
                if _did0 == 'const':
                    continue
                if pv < SIGINIFICANCE_LEVEL:
                    significant_drivers.add(_did0)
            negative_ef_drivers = set()
            for _did0, cof in res.params.iteritems():
                if _did0 == 'const':
                    continue
                if cof < 0:
                    negative_ef_drivers.add(_did0)
            #
            causalityGraph += [(int(_did0), did1) for _did0 in significant_drivers.difference(negative_ef_drivers)]
        logger.info('Pickling %s' % regressionModel_fn)
        save_pickle_file(causalityGraph_fpath, causalityGraph)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], regressionModel_fn), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()