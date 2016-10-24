import __init__
#
from community_analysis import ss_trips_dir, ss_trips_prefix
from community_analysis import tf_zone_counting_dir, tf_zone_counting_individuals_prefix, tf_zone_counting_groups_prefix
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file, check_path_exist
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
#
logger = get_logger('tf zone counting')


def run():
    logger.info('Execution')
    check_dir_create(tf_zone_counting_dir)
    #
    init_multiprocessor(8)
    count_num_jobs = 0
    for y in range(9, 13):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # yymm = '12%02d' % mm
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
        yyyy = '20%02d' % (y)
        put_task(process_file, [yyyy])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(period):
    logger.info('Handle the file; %s' % period)
    from traceback import format_exc
    try:
        ss_trips_fpath = '%s/%s%s.csv' % (ss_trips_dir, ss_trips_prefix, period)
        if not check_path_exist(ss_trips_fpath):
            logger.info('The file X exists; %s' % period)
            return None
        #
        tf_zone_counting_individuals_fpath = '%s/%s%s.pkl' % (tf_zone_counting_dir, tf_zone_counting_individuals_prefix, period)
        tf_zone_counting_groups_fpath = '%s/%s%s.pkl' % (tf_zone_counting_dir, tf_zone_counting_groups_prefix, period)
        if check_path_exist(tf_zone_counting_individuals_fpath):
            logger.info('The file had already been processed; %s' % period)
            return None
        #
        individuals, groups = {}, {}
        with open(ss_trips_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did = int(row[hid['did']])
                gn = row[hid['groupName']]
                tf, zi, zj = int(row[hid['timeFrame']]), int(row[hid['zi']]), int(row[hid['zj']])
                if not individuals.has_key(did):
                    individuals[did] = {}
                    individuals[did][tf, zi, zj] = 0
                else:
                    if not individuals[did].has_key((tf, zi, zj)):
                        individuals[did][tf, zi, zj] = 0
                individuals[did][tf, zi, zj] += 1
                #
                if not groups.has_key(gn):
                    groups[gn] = {}
                    groups[gn][tf, zi, zj] = 0
                else:
                    if not groups[gn].has_key((tf, zi, zj)):
                        groups[gn][tf, zi, zj] = 0
                groups[gn][tf, zi, zj] += 1
        logger.info('Start pickling %s' % period)
        save_pickle_file(tf_zone_counting_individuals_fpath, individuals)
        save_pickle_file(tf_zone_counting_groups_fpath, groups)
    except Exception as _:
        with open('Exception tf zone counting.txt', 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    # from taxi_common.file_handling_functions import load_pickle_file
    # print load_pickle_file('tf-zone-counting-groups-0901.pkl')
    # print load_pickle_file('tf-zone-counting-individuals-0901.pkl')
    run()
