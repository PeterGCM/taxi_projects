import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
import numpy as np
import statsmodels.api as sm
#

logger = get_logger()
sig_level = 0.10


def run():
    init_multiprocessor(6)
    count_num_jobs = 0
    tm = 'baseline'
    # for tm in ['spendingTime', 'roamingTime']:
        # for year in ['2009', '2010', '2011', '2012']:
    for year in ['2009']:
        gz_dpath = dpaths[tm, year, 'groupZones']
        check_dir_create(gz_dpath)
        #
        gt_dpath = dpaths[tm, year, 'groupTrips']
        gt_prefix = prefixs[tm, year, 'groupTrips']
        for fn in get_all_files(gt_dpath, '%s*' % gt_prefix):
            if len(fn[:-len('.csv')].split('-')) != 4:
                continue
            _, _, _, gn = fn[:-len('.csv')].split('-')
            if gn == 'X':
                continue
            gt_fpath = '%s/%s' % (gt_dpath, fn)
            # process_file(tm, year, gt_fpath)
            put_task(process_file, [tm, year, gt_fpath])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(tm, year, gt_fpath):
    gz_dpath = dpaths[tm, year, 'groupZones']
    gz_prefix = prefixs[tm, year, 'groupZones']
    df = pd.read_csv(gt_fpath)
    assert len(set(df['groupName'])) == 1
    gn = df['groupName'][0]
    gz_fpath = '%s/%s%s.pkl' % (gz_dpath, gz_prefix, gn)
    #
    tm ='spendingTime'
    df = df[~(np.abs(df[tm] - df[tm].mean()) > (3 * df[tm].std()))]
    groupZones = {}
    for zizj, pp_num in df.groupby(['zizj']).sum()['priorPresence'].iteritems():
        if pp_num < 2:
            continue
        zizj_df = df[(df['zizj'] == zizj)]
        y = zizj_df[tm]
        X = zizj_df['priorPresence']
        X = sm.add_constant(X)
        res = sm.OLS(y, X, missing='drop').fit()
        if res.params['priorPresence'] < 0 and res.pvalues['priorPresence'] < sig_level:
            groupZones[zizj] = res.params['priorPresence']
    save_pickle_file(gz_fpath, groupZones)


if __name__ == '__main__':
    run()

