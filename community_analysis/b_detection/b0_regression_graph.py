import __init__
#
'''

'''
#
from community_analysis import tfZ_SP_dpath, tfZ_SP_prepix
# from community_analysis import tfZ_RP_dpath, tfZ_RP_prepix
# from community_analysis import RP_graph_dpath, RP_graph_prefix
from community_analysis import SP_graph_dpath, SP_graph_prefix
from community_analysis import SIGINIFICANCE_LEVEL
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
import statsmodels.api as sm

logger = get_logger()


def run():
    check_dir_create(SP_graph_dpath)
    #
    # init_multiprocessor(6)
    # count_num_jobs = 0
    for y in range(9, 10):
        yyyy = '20%02d' % y
        for tfZ_RP_fn in get_all_files(tfZ_SP_dpath, '%s%s*.csv' % (tfZ_SP_prepix, yyyy)):
            tfZ_RP_fpath = '%s/%s' % (tfZ_SP_dpath, tfZ_RP_fn)
            process_file(tfZ_RP_fpath)
        # put_task(process_file, [yymm])
        # count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)

def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    print get_fn_only(fpath)
    print get_fn_only(fpath)[-len('.csv'):].split('-')
    _, _, yyyy, reducerID = get_fn_only(fpath)[-len('.csv'):].split('-')
    SP_graph_fpath = '%s/%s%s-%s.csv' % (SP_graph_dpath, SP_graph_prefix, yyyy, reducerID)
    if check_path_exist(SP_graph_fpath):
        return None
    #
    logger.info('Start loading; %s-%s' % (yyyy, reducerID))
    df = pd.read_csv(fpath)
    SP_graph = {}
    num_drivers = len(set(df['did']))
    for i, did1 in enumerate(set(df['did'])):
        #
        logger.info('Doing regression %.2f' % (i / float(num_drivers)))
        did1_df = df[(df['did'] == did1)].copy(deep=True)
        data_multi_reg = did1_df.drop(['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did', '%d' % did1], axis=1)
        candi_dummies = []
        for i, vs in enumerate(zip(*data_multi_reg.values)):
            if data_multi_reg.columns[i] == 'spendingTime':
                continue
            if sum(vs) != 0:
                candi_dummies.append(data_multi_reg.columns[i])
        y = data_multi_reg['spendingTime']
        X = data_multi_reg[candi_dummies]
        X = sm.add_constant(X)
        res = sm.OLS(y, X, missing='drop').fit()
        if res.f_pvalue >= SIGINIFICANCE_LEVEL:
            continue
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
        for _did0 in significant_drivers.difference(negative_ef_drivers):
            SP_graph[int(_did0), did1] = res.params[_did0]
    logger.info('Start pickling; %s-%s' % (yyyy, reducerID))
    save_pickle_file(SP_graph_fpath, SP_graph)


if __name__ == '__main__':
    run()
