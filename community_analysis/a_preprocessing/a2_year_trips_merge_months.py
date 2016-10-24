import __init__
#
from community_analysis import ss_trips_dir, ss_trips_prefix
#
from taxi_common.file_handling_functions import get_all_files, check_path_exist, get_modified_time
from taxi_common.log_handling_functions import get_logger
#
import csv
#
logger = get_logger('year_trip_merge_months')


def run():
    #
    for y in range(9, 13):
        ss_year_trips_fpath = '%s/%s20%02d.csv' % (ss_trips_dir, ss_trips_prefix, y)
        if check_path_exist(ss_year_trips_fpath):
            continue
        logger.info('Start handling 20%02d' % y)
        with open(ss_year_trips_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['did',
                             'timeFrame', 'zi', 'zj',
                             'groupName', 'prevDriver',
                             'time', 'day',
                             'start-long', 'start-lat',
                             'distance', 'duration', 'fare'])
            for ss_trips_fpath in get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, y), '.csv'):
                logger.info('Handling %s' % ss_trips_fpath)
                with open(ss_trips_fpath, 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    reader.next()
                    for row in reader:
                        writer.writerow(row)


if __name__ == '__main__':
    import time
    logger.info('Execution')
    while True:
        Y09 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 9), '.csv')
        Y10 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 10), '.csv')
        Y11 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 11), '.csv')
        Y12 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 12), '.csv')
        if len(Y09) == 11:
            last_fpath = '%s/%s' % (ss_trips_dir, Y09[-1])
            if time.time() - get_modified_time(last_fpath) > 5 * 60:
                run()
        if len(Y10) == 11:
            last_fpath = '%s/%s' % (ss_trips_dir, Y10[-1])
            if time.time() - get_modified_time(last_fpath) > 5 * 60:
                run()
        if len(Y11) == 7:
            last_fpath = '%s/%s' % (ss_trips_dir, Y11[-1])
            if time.time() - get_modified_time(last_fpath) > 5 * 60:
                run()
        if len(Y12) == 9:
            last_fpath = '%s/%s' % (ss_trips_dir, Y12[-1])
            if time.time() - get_modified_time(last_fpath) > 5 * 60:
                run()
        if len(Y09) == 11 and len(Y10) == 11 and len(Y11) == 7 and len(Y12) == 9:
            break
        logger.info('Falling sleep')
        time.sleep(20 * 60)


