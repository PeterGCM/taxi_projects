import __init__
#
from community_analysis import ss_trips_dir, ss_trips_prefix
from community_analysis import com_drivers_dir, com_drivers_prefix
from community_analysis import com_trips_dir, com_trips_prefix
from community_analysis import CHOSEN_PERCENTILE
from community_analysis._classes import ca_driver_with_com_prevD
from community_analysis.b_detection.b1_dw_graph_generation import generate_zones
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, check_path_exist, load_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv
#
logger = get_logger('com_trips')
percentile_dirname = 'percentile(%.3f)' % CHOSEN_PERCENTILE


def run():
    check_dir_create(com_trips_dir)
    check_dir_create('%s/%s' % (com_trips_dir, percentile_dirname))
    process_files('0901___')
    #
    # process_files(9)
    # init_multiprocessor(4)
    # count_num_jobs = 0
    # for y in range(9, 13):
    #     put_task(process_files, [y])
    #     count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def process_files(period):
    group_drivers_fpath = '%s/%s/%s%s.pkl' % (com_drivers_dir, percentile_dirname, com_drivers_prefix, period)
    group_drivers = load_pickle_file(group_drivers_fpath)
    #
    com_trips_fpath = '%s/%s/%s%s.csv' % (com_trips_dir, percentile_dirname, com_trips_prefix, period)
    if check_path_exist(com_trips_fpath):
        return None
    with open(com_trips_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['did',
                         'timeFrame', 'zi', 'zj',
                         'groupName', 'prevDriver',
                         'time', 'day',
                         'start-long', 'start-lat',
                         'distance', 'duration', 'fare'])
    #
    new_gn_assigned_trip_fpath = '%s/%s%s.csv' % (ss_trips_dir, ss_trips_prefix, period)
    logger.info('Start handing %s' % new_gn_assigned_trip_fpath)
    did_gn, drivers = {}, {}
    num_groups = 0
    for gn, members in group_drivers.iteritems():
        num_groups += 1
        for did in members:
            did_gn[did] = gn
            drivers[did] = ca_driver_with_com_prevD(did, members)
    zones = generate_zones()
    handling_day = 0
    with open(new_gn_assigned_trip_fpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            did = int(row[hid['did']])
            t = eval(row[hid['time']])
            day = int(row[hid['day']])
            zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
            z = zones[(zi, zj)]
            if handling_day < day:
                logger.info('%dth handing %s' % (day, new_gn_assigned_trip_fpath))
                handling_day = day
            if not drivers.has_key(did):
                drivers[did] = ca_driver_with_com_prevD(did, [])
                did_gn[did] = 'G(%d)' % num_groups
                num_groups += 1
            prev_com_driver = drivers[did].find_prevDriver(t, z)
            #
            gn = did_gn[did]
            with open(com_trips_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = [did,
                           row[hid['timeFrame']], zi, zj,
                           gn, prev_com_driver,
                           t, day,
                           row[hid['start-long']], row[hid['start-lat']],
                           row[hid['distance']], row[hid['duration']], row[hid['fare']]]
                writer.writerow(new_row)


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception com trips.txt', 'w') as f:
            f.write(format_exc())
        raise