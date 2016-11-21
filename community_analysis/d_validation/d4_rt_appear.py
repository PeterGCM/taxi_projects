import __init__
#
'''

'''
#
from community_analysis import rt_day_dir
from community_analysis import tf_zone_drivers_dir, tf_zone_drivers_prefix
from community_analysis import rt_appear_dir, rt_appear_prefix
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, get_all_files, load_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime

logger = get_logger('rt_appear')


def run():
    check_dir_create(rt_appear_dir)
    #
    init_multiprocessor(4)
    count_num_jobs = 0
    for y in range(9, 13):
        yyyy = '20%02d' % y
        # process_file(yyyy)
        put_task(process_file, [yyyy])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(period):
    from traceback import format_exc
    #
    try:
        logger.info('Handle %s' % period)
        rt_appear_fpath = '%s/%s%s.csv' % (rt_appear_dir, rt_appear_prefix, period)
        if check_path_exist(rt_appear_fpath):
            logger.info('Already handled %s' % period)
            return None
        logger.info('Generate year roaming time %s' % period)
        driver_roaming_time = {}
        drivers = set()
        for fn in get_all_files(rt_day_dir, '', '.csv'):
            month_fpath = '%s/%s' % (rt_day_dir, fn)
            with open(month_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    did = int(row[hid['did']])
                    t = eval(row[hid['time']])
                    cur_dt = datetime.datetime.fromtimestamp(t)
                    k = (did, cur_dt.month, cur_dt.day, row[hid['timeFrame']], row[hid['zi']], row[hid['zj']])
                    driver_roaming_time[k] = eval(row[hid['roamingTime']])
                    drivers.add(did)
        #
        logger.info('load year drivers appear %s' % period)
        tf_zone_drivers_fpath = '%s/%s%s.pkl' % (tf_zone_drivers_dir, tf_zone_drivers_prefix, period)
        year_drivers_appear = load_pickle_file(tf_zone_drivers_fpath)
        #
        logger.info('start rt appear summary %s' % period)
        with open(rt_appear_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['month', 'day', 'timeFrame', 'zi', 'zj', 'did', 'roamingTime']
            for did in drivers:
                header.append('%d' % did)
            writer.writerow(header)
        for (did1, month, day, tf, zi, zj), roaming_time in driver_roaming_time.iteritems():
            new_row = [month, day, tf, zi, zj, did1, roaming_time]
            for did0 in drivers:
                was_there = 1 if did0 in year_drivers_appear[(did0, month, day, tf, zi, zj)] else 0
                new_row.append(was_there)
            with open(rt_appear_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], period), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()