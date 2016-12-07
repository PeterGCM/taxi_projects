import __init__
#
'''

'''
#
from community_analysis import ss_trips_dpath, ss_trips_prefix
from community_analysis import tfZ_counting_dpath, tfZ_counting_individuals_prefix, tfZ_counting_groups_prefix
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file, check_path_exist
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
#
logger = get_logger()


def run():
    logger.info('Execution')
    check_dir_create(tfZ_counting_dpath)
    #
    init_multiprocessor(8)
    count_num_jobs = 0
    for y in range(9, 13):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # process_file(yymm)
            put_task(process_month, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_month(yymm):
    logger.info('Handle the file; %s' % yymm)
    from traceback import format_exc
    try:
        ss_trips_fpath = '%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, yymm)
        if not check_path_exist(ss_trips_fpath):
            logger.info('The file X exists; %s' % yymm)
            return None
        #
        tf_zone_counting_individuals_fpath = '%s/%s%s.pkl' % (tfZ_counting_dpath, tfZ_counting_individuals_prefix, yymm)
        tf_zone_counting_groups_fpath = '%s/%s%s.pkl' % (tfZ_counting_dpath, tfZ_counting_groups_prefix, yymm)
        if check_path_exist(tf_zone_counting_individuals_fpath):
            logger.info('The file had already been processed; %s' % yymm)
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
        logger.info('Start pickling %s' % yymm)
        save_pickle_file(tf_zone_counting_individuals_fpath, individuals)
        save_pickle_file(tf_zone_counting_groups_fpath, groups)
    except Exception as _:
        with open('Exception tf zone counting.txt', 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
