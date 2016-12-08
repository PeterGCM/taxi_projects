import __init__
#
'''

'''
#
from community_analysis import FRI, SAT, SUN
from community_analysis import PM2, PM11
from community_analysis import taxi_home
from community_analysis import ss_trips_dpath, ss_trips_prefix
from community_analysis import group_dpath, group_prepix
#
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create, check_path_exist, get_all_directories
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
#
from bisect import bisect
import csv, datetime
#
logger = get_logger()


def run():
    check_dir_create(ss_trips_dpath)
    #
    # init_multiprocessor(11)
    # count_num_jobs = 0
    for y in range(9, 10):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # initial_processing(yymm)
            # put_task(initial_processing, [yymm])
            group_defined_processing(yymm)
            # put_task(group_defined_processing, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def group_defined_processing(yymm):
    for wc in get_all_directories(group_dpath):
        ss_trips_wc_dpath = '%s/%s' % (ss_trips_dpath, wc)
        check_dir_create(ss_trips_wc_dpath)
    #
    for wc in get_all_directories(group_dpath):
        if wc != 'fb':
            continue
        ss_trips_wc_dpath = '%s/%s' % (ss_trips_dpath, wc)
        ss_trips_wc_fpath = '%s/%s%s-%s.csv' % (ss_trips_wc_dpath, ss_trips_prefix, wc, yymm)
        if check_path_exist(ss_trips_wc_fpath):
            logger.info('The file had already been processed; %s' % ss_trips_wc_fpath)
            continue
        with open(ss_trips_wc_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['did',
                             'timeFrame', 'zi', 'zj',
                             'groupName', 'prevDriver',
                             'time', 'day',
                             'start-long', 'start-lat',
                             'distance', 'duration', 'fare'])
        #
        logger.info('Process wc-yymm; %s-%s' % (wc, yymm))
        yyyy = '20%s' % (yymm[:2])
        group_wc_dpath = '%s/%s' % (group_dpath, wc)
        group_drivers_fpath = '%s/%s%s-%s-drivers.pkl' % (group_wc_dpath, group_prepix, wc, yyyy)
        group_drivers = load_pickle_file(group_drivers_fpath)
        ss_trips_fpath = '%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, yymm)
        with open(ss_trips_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            handling_day = 0
            for row in reader:
                did = int(row[hid['did']])
                gn = None
                for gn0, drivers in group_drivers.iteritems():
                    if did in drivers:
                        gn = gn0
                        break
                if not gn:
                    continue
                t = eval(row[hid['time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                day = cur_dt.day
                if handling_day != day:
                    handling_day = day
                    logger.info('handling; %s-%d' % (yymm, handling_day))
                tf = int(row[hid['timeFrame']])
                zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                with open(ss_trips_wc_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([did,
                                     tf, zi, zj,
                                     gn, 'None',
                                     t, cur_dt.day,
                                     row[hid['start-long']], row[hid['start-lat']],
                                     row[hid['distance']], row[hid['duration']], row[hid['fare']]
                                     ])


def initial_processing(yymm):
    logger.info('handle the file; %s' % yymm)
    yy, mm = yymm[:2], yymm[2:]
    normal_fpath = '%s/20%s/%s/trips/trips-%s-normal.csv' % (taxi_home, yy, mm, yymm)
    ext_fpath = '%s/20%s/%s/trips/trips-%s-normal-ext.csv' % (taxi_home, yy, mm, yymm)
    if not check_path_exist(normal_fpath):
        logger.info('The file X exists; %s' % yymm)
        return None
    ftd_list_fpath = '%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm)
    if not check_path_exist(ftd_list_fpath):
        return None
    ft_drivers = load_pickle_file(ftd_list_fpath)
    x_points, y_points = get_sg_grid_xy_points()
    #
    ss_trips_fpath = '%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, yymm)
    if check_path_exist(ss_trips_fpath):
        logger.info('The file had already been processed; %s' % yymm)
        return None
    with open(ss_trips_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['did',
                         'timeFrame', 'zi', 'zj',
                         'groupName', 'prevDriver',
                         'time', 'day',
                         'start-long', 'start-lat',
                         'distance', 'duration', 'fare'])
    drivers = {}
    with open(normal_fpath, 'rb') as r_csvfile1:
        reader1 = csv.reader(r_csvfile1)
        headers1 = reader1.next()
        # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
        #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
        #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
        #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
        #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}
        hid1 = {h: i for i, h in enumerate(headers1)}
        with open(ext_fpath, 'rb') as r_csvfile2:
            reader2 = csv.reader(r_csvfile2)
            headers2 = reader2.next()
            # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
            hid2 = {h: i for i, h in enumerate(headers2)}
            #
            handling_day = 0
            for row1 in reader1:
                row2 = reader2.next()
                did = row2[hid2['driver-id']]
                if did == '-1':
                    continue
                #
                if did not in ft_drivers:
                    continue
                t = eval(row1[hid1['start-time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                if handling_day != cur_dt.day:
                    handling_day = cur_dt.day
                    logger.info('Processing %s %dth day' % (yymm, cur_dt.day))
                if cur_dt.weekday() in [FRI, SAT, SUN]:
                    continue
                if cur_dt.hour < PM2:
                    continue
                if PM11 < cur_dt.hour:
                    continue
                #
                s_long, s_lat = eval(row1[hid1['start-long']]), eval(row1[hid1['start-lat']])
                zi, zj = bisect(x_points, s_long) - 1, bisect(y_points, s_lat) - 1
                if zi < 0 or zj < 0:
                    continue
                #
                if not drivers.has_key(did):
                    drivers[did] = 'G(%d)' % len(drivers)
                gn = drivers[did]
                with open(ss_trips_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([did,
                                     cur_dt.hour, zi, zj,
                                     gn, 'None',
                                     t, cur_dt.day,
                                     row1[hid1['start-long']], row1[hid1['start-lat']],
                                     row1[hid1['distance']], row1[hid1['duration']], row1[hid1['fare']]
                                     ])


if __name__ == '__main__':
    run()
