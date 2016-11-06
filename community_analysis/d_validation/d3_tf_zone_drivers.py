import __init__
#
from community_analysis import com_drivers_dir, com_drivers_prefix
from community_analysis import com_trips_dir, com_trips_prefix
from community_analysis import tf_zone_drivers_dir, tf_zone_drivers_prefix
from community_analysis import CHOSEN_PERCENTILE
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv

logger = get_logger('tf_zone_drivers')
percentile_dirname = 'percentile(%.3f)' % CHOSEN_PERCENTILE


def run():
    check_dir_create(tf_zone_drivers_dir)
    #
    process_file('0901')
    # init_multiprocessor(8)
    # count_num_jobs = 0
    # for y in range(9, 10):
    #     for m in range(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         # yymm = '12%02d' % mm
    #         # process_file(yymm)
    #         put_task(process_file, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def process_file(period):
    from traceback import format_exc
    #
    try:
        tf_zone_drivers_fpath = '%s/%s%s.csv' % (tf_zone_drivers_dir, tf_zone_drivers_prefix, period)
        if check_path_exist(tf_zone_drivers_fpath):
            logger.info('Already handled; %s' % period)
            return None
        group_drivers_fpath = '%s/%s/%s%s.pkl' % (com_drivers_dir, percentile_dirname, com_drivers_prefix, period)
        if not check_path_exist(group_drivers_fpath):
            logger.info('The file X exists; %s' % period)
            return None
        com_trips_fpath = '%s/%s/%s%s.csv' % (com_trips_dir, percentile_dirname, com_trips_prefix, period)
        with open(com_trips_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            row = reader.next()
            handling_day = int(row[hid['day']])
            tf_zone_drivers = {}
            while row:
                day = int(row[hid['day']])
                if handling_day != day:
                    logger.info('finished; %s-%d' % (period, handling_day))
                    handling_day = day
                did = int(row[hid['did']])
                tf = int(row[hid['timeFrame']])
                zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                k = (day, tf, zi, zj)
                if not tf_zone_drivers.has_key(k):
                    tf_zone_drivers[k] = set()
                tf_zone_drivers[k].add(did)
                #
                row = reader.next()
        save_pickle_file(tf_zone_drivers_fpath, tf_zone_drivers)
    except Exception as _:
        with open('tf_zone_drivers_%s.txt' % period, 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()