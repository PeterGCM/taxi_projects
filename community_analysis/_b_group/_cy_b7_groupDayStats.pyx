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
    # tm = 'spendingTime'
    tm = 'baseline'
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
                  'numTrips', 'proDur','fare', 'fare/Trip', 'distance/Trip', 'duration/Trip', 'spendingTime', 'spendingTime/Trip',
                  'priorOnumTrips', 'priorO_ST', 'priorO_ST/Trip',
                  'priorXnumTrips', 'priorX_ST', 'priorX_ST/Trip']
        writer.writerow(header)
    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    gs_dpath = dpaths[tm, year, 'groupShifts']
    gs_prefix = prefixs[tm, year, 'groupShifts']

    for fn in get_all_files(gt_dpath, '%s*.csv' % gt_prefix):
        if len(fn[:-len('.csv')].split('-')) != 4:
            continue
        _, _, _, gn = fn[:-len('.csv')].split('-')
        gt_fpath = '%s/%s' % (gt_dpath, fn)
        gs_fpath = '%s/%s%s.csv' % (gs_dpath, gs_prefix, gn)
        gt_df = pd.read_csv(gt_fpath)
        gs_df = pd.read_csv(gs_fpath)
        numDrivers = len(set(gt_df['did']))
        numTrips = gt_df.groupby(['year', 'month', 'day', 'did']).count().reset_index()['groupName'].mean()
        proDur = gs_df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['pro-dur'].mean()
        distance = gt_df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['distance'].mean()
        duration = gt_df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['duration'].mean()
        fare = gt_df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['fare'].mean()
        distance_trip = distance / float(numTrips)
        duration_trip = duration / float(numTrips)
        fare_trip = fare / float(numTrips)
        spendingTime = gt_df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['spendingTime'].mean()
        spendingTime_trip = spendingTime / float(numTrips)
        #
        priorO_gt_df = gt_df[(gt_df['priorPresence'] == 1)]
        priorOnumTrips = priorO_gt_df.groupby(['year', 'month', 'day', 'did']).count().reset_index()['groupName'].mean()
        priorO_ST = priorO_gt_df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['spendingTime'].mean()
        priorO_ST_trip = priorO_ST / float(priorOnumTrips)
        #
        priorX_gt_df = gt_df[(gt_df['priorPresence'] == 0)]
        priorXnumTrips = priorX_gt_df.groupby(['year', 'month', 'day', 'did']).count().reset_index()['groupName'].mean()
        priorX_ST = priorX_gt_df.groupby(['year', 'month', 'day', 'did']).sum().reset_index()['spendingTime'].mean()
        priorX_ST_trip = priorX_ST / float(priorXnumTrips)


        with open(gds_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [gn, numDrivers,
                      numTrips, proDur, fare, fare_trip, distance_trip, duration_trip, spendingTime, spendingTime_trip,
                       priorOnumTrips, priorO_ST, priorO_ST_trip,
                       priorXnumTrips, priorX_ST, priorX_ST_trip]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()
