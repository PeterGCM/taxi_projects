import __init__
#
'''

'''
#
from community_analysis import ss_trips_dpath, ss_trips_prefix
#
from taxi_common.file_handling_functions import get_all_files, check_path_exist, get_modified_time
from taxi_common.log_handling_functions import get_logger
#
import csv
#
logger = get_logger('year_trip_merge_months')


def run():
    #
    for y in range(10, 13):
        ss_year_trips_fpath = '%s/%s20%02d.csv' % (ss_trips_dpath, ss_trips_prefix, y)
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
            drivers = {}
            for ss_trips_fpath in get_all_files(ss_trips_dpath, '%s%02d' % (ss_trips_prefix, y), '.csv'):
                logger.info('Handling %s' % ss_trips_fpath)
                with open('%s/%s' % (ss_trips_dpath, ss_trips_fpath), 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    hid = {h: i for i, h in enumerate(headers)}
                    for row in reader:
                        did = row[hid['did']]
                        if not drivers.has_key(did):
                            drivers[did] = 'G(%d)' % len(drivers)
                        gn = drivers[did]
                        writer.writerow([did,
                                         row[hid['timeFrame']], row[hid['zi']], row[hid['zj']],
                                         gn, row[hid['prevDriver']],
                                         row[hid['time']], row[hid['day']],
                                         row[hid['start-long']], row[hid['start-lat']],
                                         row[hid['distance']], row[hid['duration']], row[hid['fare']]])


if __name__ == '__main__':
    run()


    # import time
    # logger.info('Execution')
    # MODI_TH = 5 * 60
    # while True:
    #     Y09 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 9), '.csv')
    #     Y10 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 10), '.csv')
    #     Y11 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 11), '.csv')
    #     Y12 = get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, 12), '.csv')
    #     if len(Y09) == 11:
    #         last_modi_time = -1e400
    #         for fn in Y09:
    #             fpath = '%s/%s' % (ss_trips_dir, fn)
    #             if last_modi_time < get_modified_time(fpath):
    #                 last_modi_time = get_modified_time(fpath)
    #         if time.time() - last_modi_time > MODI_TH:
    #             run()
    #     if len(Y10) == 11:
    #         last_modi_time = -1e400
    #         for fn in Y10:
    #             fpath = '%s/%s' % (ss_trips_dir, fn)
    #             if last_modi_time < get_modified_time(fpath):
    #                 last_modi_time = get_modified_time(fpath)
    #         if time.time() - last_modi_time > MODI_TH:
    #             run()
    #     if len(Y11) == 7:
    #         last_modi_time = -1e400
    #         for fn in Y11:
    #             fpath = '%s/%s' % (ss_trips_dir, fn)
    #             if last_modi_time < get_modified_time(fpath):
    #                 last_modi_time = get_modified_time(fpath)
    #         if time.time() - last_modi_time > MODI_TH:
    #             run()
    #     if len(Y12) == 9:
    #         last_modi_time = -1e400
    #         for fn in Y12:
    #             fpath = '%s/%s' % (ss_trips_dir, fn)
    #             if last_modi_time < get_modified_time(fpath):
    #                 last_modi_time = get_modified_time(fpath)
    #         if time.time() - last_modi_time > MODI_TH:
    #             run()
    #     for y in range(9, 13):
    #         ss_year_trips_fpath = '%s/%s20%02d.csv' % (ss_trips_dir, ss_trips_prefix, y)
    #         if not check_path_exist(ss_year_trips_fpath):
    #             break
    #     else:
    #         break
    #     logger.info('Falling sleep')
    #     time.sleep(20 * 60)


