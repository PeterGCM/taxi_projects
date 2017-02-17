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
    # init_multiprocessor(4)
    # count_num_jobs = 0
    tm = 'spendingTime'
    # for year in ['2009', '2010', '2011', '2012']:
    for year in ['2009']:
        gds_dpath = dpaths[tm, year, 'groupDayStats']
        check_dir_create(gds_dpath)
        #
        process_file(tm, year)
    #     put_task(process_file, [tm, year])
    #     count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def process_file(tm, year):
    logger.info('handle the file; %s-%s' % (tm, year))
    gds_dpath = dpaths[tm, year, 'groupDayStats']
    gds_prefix = prefixs[tm, year, 'groupDayStats']
    gds_fpath = '%s/%s%s.csv' % (gds_dpath, gds_prefix, 'summary')
    with open(gds_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['groupName', 'numDrivers',
                  'numTrips', 'fare', 'fare/Trip', 'spendingTime', 'spendingTime/Trip']
        writer.writerow(header)
    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    for fn in get_all_files(gt_dpath, '%s*.csv' % gt_prefix):
        if len(fn[:-len('.csv')].split('-')) != 4:
            continue
        _, _, _, gn = fn[:-len('.csv')].split('-')
        gt_fpath = '%s/%s' % (gt_dpath, fn)
        df = pd.read_csv(gt_fpath)
        numDrivers = len(set(df['did']))
        numTrips = df.groupby(['year', 'month', 'day', 'did']).count().reset_index()['groupName'].mean()
        fare = df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['fare'].mean()
        fare_trip = fare / float(numTrips)
        spendingTime = df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['spendingTime'].mean()
        spendingTime_trip = spendingTime / float(numTrips)
        with open(gds_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [gn, numDrivers,
                      numTrips, fare, fare_trip, spendingTime, spendingTime_trip]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()
