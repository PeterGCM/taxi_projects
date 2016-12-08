import __init__
#
'''

'''
#
from taxi_common import get_taxi_home_path
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
#
from file_handling_functions import check_dir_create, check_path_exist, save_pickle_file, load_pickle_file
from log_handling_functions import get_logger
from multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv

logger = get_logger()


def run():
    check_dir_create(ss_drivers_dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 10):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            # process_file(yymm)
            put_task(process_month, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

    # for y in xrange(9, 10):
    #     yyyy = '20%02d' % y
    #     process_year(yyyy)


def process_year(yyyy):
    ss_drivers_year_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yyyy)
    if check_path_exist(ss_drivers_year_fpath):
        logger.info('Already handled; %s' % yyyy)
        return None
    yy = yyyy[2:]
    ss_drivers_year = None
    for m in xrange(1, 13):
        yymm = '%s%02d' % (yy, m)
        ss_drivers_month_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yymm)
        if not check_path_exist(ss_drivers_month_fpath):
            logger.info('The file X exists; %s' % yymm)
            return None
            ss_drivers_month = load_pickle_file(ss_drivers_month_fpath)
            if not ss_drivers_year:
                ss_drivers_year = ss_drivers_month
            else:
                ss_drivers_year.intersection_update(set(ss_drivers_month))
    save_pickle_file(ss_drivers_year_fpath, ss_drivers_year)


def process_month(yymm):
    logger.info('handle the file; %s' % yymm)
    yy, mm = yymm[:2], yymm[2:]
    normal_fpath = '%s/20%s/%s/trips/trips-%s-normal.csv' % (get_taxi_home_path(), yy, mm, yymm)
    ext_fpath = '%s/20%s/%s/trips/trips-%s-normal-ext.csv' % (get_taxi_home_path(), yy, mm, yymm)
    if not check_path_exist(normal_fpath):
        logger.info('The file X exists; %s' % yymm)
        return None
    ss_drivers_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yymm)
    if check_path_exist(ss_drivers_fpath):
        logger.info('Already handled; %s' % yymm)
        return None
    vehicle_sharing = {}
    with open(normal_fpath, 'rb') as r_csvfile1:
        reader1 = csv.reader(r_csvfile1)
        headers1 = reader1.next()
        #
        # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
        #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
        #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
        #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
        #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}
        #
        hid1 = {h: i for i, h in enumerate(headers1)}
        with open(ext_fpath, 'rb') as r_csvfile2:
            reader2 = csv.reader(r_csvfile2)
            headers2 = reader2.next()
            #
            # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
            #
            hid2 = {h: i for i, h in enumerate(headers2)}
            for row1 in reader1:
                row2 = reader2.next()
                did = int(row2[hid2['driver-id']])
                if did == int('-1'):
                    continue
                vid = int(row1[hid1['vehicle-id']])
                if not vehicle_sharing.has_key(vid):
                    vehicle_sharing[vid] = set()
                vehicle_sharing[vid].add(did)
    #
    logger.info('Filtering single-shift drivers; %s' % yymm)
    ss_drivers = set()
    for vid, drivers in vehicle_sharing.iteritems():
        if len(drivers) > 1:
            continue
        did = drivers.pop()
        assert len(drivers) == 0
        ss_drivers.add(did)
    save_pickle_file(ss_drivers_fpath, ss_drivers)

if __name__ == '__main__':
    run()