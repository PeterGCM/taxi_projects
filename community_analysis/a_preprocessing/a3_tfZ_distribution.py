import __init__
#
'''

'''
#
from community_analysis import tfZ_counting_dpath
from community_analysis import tfZ_counting_individuals_prefix, tfZ_counting_groups_prefix
from community_analysis import tfZ_distribution_dpath
from community_analysis import tfZ_distribution_individuals_prefix, tfZ_distribution_groups_prefix, \
                                tfZ_distribution_whole_prefix
from community_analysis import PM2, PM11
#
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file, \
                            save_pickle_file, save_pkl_threading, get_all_files, check_path_exist
from taxi_common.sg_grid_zone import get_sg_zones
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
#
logger = get_logger()


def run():
    check_dir_create(tfZ_distribution_dpath)
    #
    # init_multiprocessor(8)
    # count_num_jobs = 0
    # for y in range(9, 13):
    #     for m in range(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         # process_file(yymm)
    #         put_task(process_individual_group, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)
    #
    for y in range(9, 10):
        yyyy = '20%02d' % y
        process_whole_distribution(yyyy)


def process_whole_distribution(yyyy):
    logger.info('Start process_whole_distribution %s' % yyyy)
    whole_distribution_fpath = '%s/%s%s.csv' % (tfZ_distribution_dpath, tfZ_distribution_whole_prefix, yyyy)
    if check_path_exist(whole_distribution_fpath):
        logger.info('Already handled %s' % yyyy)
        return
    whole_counting = {}
    for m in range(1, 13):
        yymm = yyyy[2:] + '%02d' % m
        logger.info('Loading and processing %s' % yymm)
        individual_tfZ_counting_fpath = '%s/%s%s.pkl' % (tfZ_counting_dpath, tfZ_counting_individuals_prefix, yymm)
        if not check_path_exist(individual_tfZ_counting_fpath):
            continue
        for did, tfZ_counting in load_pickle_file(individual_tfZ_counting_fpath):
            for tfZ, num_trips in tfZ_counting.iteritems():
                if not whole_counting.has_key(tfZ):
                    whole_counting[tfZ] = 0
                whole_counting[tfZ] += num_trips
    whole_distribution = {}
    year_num_trips = sum(whole_counting.values())
    for tfZ, tf_zone_counting in whole_counting.iteritems():
        whole_distribution[tfZ] = tf_zone_counting / float(year_num_trips)
    #
    headers = ['k', 'timeFrame', 'zid', 'probability']
    LK, LTF, LZ, LP = range(4)
    zones = get_sg_zones()
    df_data = {k: [] for k in headers}
    for tf in range(PM2, PM11 + 1):
        for (i, j) in zones.iterkeys():
            if i < 0 or j < 0:
                continue
            k = (tf, i, j)
            prob = whole_distribution[k] if whole_distribution.has_key(k) else 0
            df_data[headers[LK]].append(k)
            df_data[headers[LTF]].append(tf)
            df_data[headers[LZ]].append('z%03d%03d' % (i, j))
            df_data[headers[LP]].append(prob)
    df = pd.DataFrame(df_data)[headers]
    df.to_csv(whole_distribution_fpath, index=False)


def process_individual_group(yymm):
    logger.info('Start process_individual_group %s' % yymm)
    individual_dist_fpath = '%s/%s%s.pkl' % (tfZ_distribution_dpath, tfZ_distribution_individuals_prefix, yymm)
    if check_path_exist(individual_dist_fpath):
        logger.info('Already handled %s' % yymm)
        return
    #
    logger.info('Processing individual distribution %s' % yymm)
    individual_tfZ_counting_fpath = '%s/%s%s.pkl' % (tfZ_counting_dpath, tfZ_counting_individuals_prefix, yymm)
    individual_distribution = {}
    for did, tfZ_counting in load_pickle_file(individual_tfZ_counting_fpath):
        total_num_trips = sum(tfZ_counting.values())
        individual_distribution[did] = {}
        for tf_zone, num_trips in tfZ_counting.iteritems():
            individual_distribution[did][tf_zone] = num_trips / float(total_num_trips)
    save_pkl_threading(individual_tfZ_counting_fpath, individual_distribution)
    #
    logger.info('Processing individual distribution %s' % yymm)
    group_tfZ_counting_fpath = '%s/%s%s.pkl' % (tfZ_counting_dpath, tfZ_counting_groups_prefix, yymm)
    group_distribution = {}
    for gn, tfZ_counting in load_pickle_file(group_tfZ_counting_fpath):
        total_num_trips = sum(tfZ_counting.values())
        group_distribution[gn] = {}
        for tf_zone, num_trips in tfZ_counting.iteritems():
            group_distribution[gn][tf_zone] = num_trips / float(total_num_trips)
    distribution_fpath = '%s/%s%s.pkl' % (tfZ_distribution_dpath, tfZ_distribution_groups_prefix, yymm)
    save_pickle_file(distribution_fpath, group_distribution)


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception tf zone distribution', 'w') as f:
            f.write(format_exc())
        raise