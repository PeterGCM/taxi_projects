import __init__
#
'''

'''
#
from community_analysis import ss_trips_dpath, ss_trips_prefix
from community_analysis import group_dpath, group_prepix
from community_analysis import pickUp_dpath, pickUp_prepix
from community_analysis import pickUpY2_dpath, pickUpY2_prepix
#
from taxi_common.file_handling_functions import check_dir_create, get_all_directories, check_path_exist, load_pickle_file, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
logger = get_logger()


def run():
    check_dir_create(pickUpY2_dpath)
    for wc in get_all_directories(group_dpath):
        pickUp_wc_dpath = '%s/%s' % (pickUpY2_dpath, wc)
        check_dir_create(pickUp_wc_dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in range(9, 11):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # yymm = '12%02d' % mm
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(period):
    from traceback import format_exc
    try:
        logger.info('handle period; %s' % period)
        ss_trips_fpath = '%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, period)
        if not check_path_exist(ss_trips_fpath):
            logger.info('The file X exists; %s' % ss_trips_fpath)
            return None
        #
        logger.info('load group drivers; %s' % period)

        # yyyy = '20%s' % (period[:2])
        yyyy2 ='20092010'

        wc_group_drivers = {}
        for wc in get_all_directories(group_dpath):
            pickUp_wc_dpath = '%s/%s' % (pickUpY2_dpath, wc)
            pickUp_fpath = '%s/%s%s-%s.pkl' % (pickUp_wc_dpath, pickUpY2_prepix, wc, period)
            if check_path_exist(pickUp_fpath):
                logger.info('The file had already been processed; %s' % pickUp_fpath)
                continue
            group_wc_dpath = '%s/%s' % (group_dpath, wc)
            # group_drivers_fpath = '%s/%s%s-%s-drivers.pkl' % (group_wc_dpath, group_prepix, wc, yyyy)
            group_drivers_fpath = '%s/%s%s-%s-drivers.pkl' % (group_wc_dpath, group_prepix, wc, yyyy2)
            group_drivers = load_pickle_file(group_drivers_fpath)
            wc_group_drivers[wc] = group_drivers
        #
        logger.info('Process checking pickUp; %s' % period)
        wc_gd_pickUp = {k: set() for k in wc_group_drivers.iterkeys()}
        with open(ss_trips_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            handling_day = 0
            for row in reader:
                t = eval(row[hid['time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                day = cur_dt.day
                if handling_day != day:
                    handling_day = day
                    logger.info('handling; %s-%d' % (period, handling_day))
                did = int(row[hid['did']])
                tf = int(row[hid['timeFrame']])
                zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                k = (did, cur_dt.month, day, tf, zi, zj)
                for wc, group_drivers in wc_group_drivers.iteritems():
                    for drivers in group_drivers.itervalues():
                        if did in drivers:
                            wc_gd_pickUp[wc].add(k)
                            break
        #
        logger.info('Pickling; %s' % period)
        for wc, gd_pickUp in wc_gd_pickUp.iteritems():
            pickUp_wc_dpath = '%s/%s' % (pickUpY2_dpath, wc)
            pickUp_fpath = '%s/%s%s-%s.pkl' % (pickUp_wc_dpath, pickUpY2_prepix, wc, period)
            save_pickle_file(pickUp_fpath, gd_pickUp)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], period), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
