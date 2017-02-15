import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
import igraph as ig
import csv
#
logger = get_logger()


def run():
    init_multiprocessor(6)
    count_num_jobs = 0
    for tm in ['spendingTime']:
        for year in ['2009', '2010', '2011', '2012']:
            gm_dpath = dpaths[tm, year, 'groupMarginal']
            check_dir_create(gm_dpath)
            #
            gp_dpath = dpaths[tm, year, 'groupPartition']
            gp_prefix = prefixs[tm, year, 'groupPartition']
            for fn in get_all_files(gp_dpath, '%s*.pkl' % gp_prefix):
                _, _, _, gn = fn[:-len('.pkl')].split('-')
                if gn == 'drivers' or gn == 'original':
                    continue
                # process_file(tm, year, gn)
                put_task(process_file, [tm, year, gn])
                count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(tm, year, gn):
    logger.info('handle the file; %s-%s-%s' % (tm, year, gn))
    gm_dpath = dpaths[tm, year, 'groupMarginal']
    gm_prefix = prefixs[tm, year, 'groupMarginal']
    gm_fpath = '%s/%s%s.csv' % (gm_dpath, gm_prefix, gn)
    with open(gm_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['groupName','did0', 'did1', 'coef', 'numTrips', 'margianlContribution']
        writer.writerow(header)
    #
    gp_dpath = dpaths[tm, year, 'groupPartition']
    gp_prefix = prefixs[tm, year, 'groupPartition']
    gp_fpath = '%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn)
    igG = ig.Graph.Read_Pickle(gp_fpath)
    #
    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    num_gt_fpath = '%s/%snum-%s.csv' % (gt_dpath, gt_prefix, gn)
    df = pd.read_csv(num_gt_fpath)
    #
    for e in igG.es:
        did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
        coef = e['weight']
        numTrips = len(df[(df['did0'] == did0) & (df['did1'] == did1)])
        margianlContribution = coef * numTrips
        with open(gm_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([gn,did0, did1, coef, numTrips, margianlContribution])


if __name__ == '__main__':
    run()

