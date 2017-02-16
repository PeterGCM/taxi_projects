import __init__
'''
'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import pandas as pd


logger = get_logger()

def run():
    init_multiprocessor(6)
    count_num_jobs = 0
    tm = 'spendingTime'
    for year in ['2009', '2010', '2011', '2012']:
        gds_dpath = dpaths[tm, year, 'groupDriverStats']
        check_dir_create(gds_dpath)
        #
        gm_dpath = dpaths[tm, year, 'groupMarginal']
        gm_prefix = prefixs[tm, year, 'groupMarginal']
        for fn in get_all_files(gm_dpath, '%s*.csv' % gm_prefix):
            _, _, _, gn = fn[:-len('.csv')].split('-')
            # process_file(tm, year, gn)
            put_task(process_file, [tm, year, gn])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(tm, year, gn):
    logger.info('handle the file; %s-%s-%s' % (tm, year, gn))
    gds_dpath = dpaths[tm, year, 'groupDriverStats']
    gds_prefix = prefixs[tm, year, 'groupDriverStats']
    gds_fpath = '%s/%s%s.csv' % (gds_dpath, gds_prefix, gn)
    with open(gds_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['did',
                  'numTrips', 'numPriorPresence', 'numXPresence', 'priorPresenceRatio',
                  'totalContribution', 'ratioContribution',
                  'totalBenefit', 'ratioBenefit']
        writer.writerow(header)
    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    gt_fpath = '%s/%s%s.csv' % (gt_dpath, gt_prefix, gn)
    gm_dpath = dpaths[tm, year, 'groupMarginal']
    gm_prefix = prefixs[tm, year, 'groupMarginal']
    gm_fpath = '%s/%s%s.csv' % (gm_dpath, gm_prefix, gn)
    #
    gt_df = pd.read_csv(gt_fpath)
    gm_df = pd.read_csv(gm_fpath)
    groupSumContiribution = gm_df['margianlContribution'].sum()
    drivers = set(gt_df['did'])
    for did in drivers:
        did_gt_df = gt_df[(gt_df['did'] == did)]
        numTrips = len(did_gt_df)
        numPriorPresence = len(did_gt_df[(did_gt_df['priorPresence'] == 1)])
        numXPresence = numTrips - numPriorPresence
        priorPresenceRatio = numPriorPresence / float(numTrips)
        #
        did0_gm_df = gm_df[(gm_df['did0'] == did)]
        if len(did0_gm_df) == 0:
            totalContribution, ratioContribution = 0, 0
        else:
            totalContribution = did0_gm_df['margianlContribution'].sum()
            ratioContribution = totalContribution / float(groupSumContiribution)
        did1_gm_df = gm_df[(gm_df['did1'] == did)]
        if len(did1_gm_df) == 0:
            totalBenefit, ratioBenefit = 0, 0
        else:
            totalBenefit = did1_gm_df['margianlContribution'].sum()
            ratioBenefit = totalBenefit / float(groupSumContiribution)
        with open(gds_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [did,
                       numTrips, numPriorPresence, numXPresence, priorPresenceRatio,
                       totalContribution, ratioContribution,
                       totalBenefit, ratioBenefit]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()
