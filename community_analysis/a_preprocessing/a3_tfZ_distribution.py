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
#
import pandas as pd
#
logger = get_logger('tf zone distribution')


def run():
    logger.info('Execution')
    check_dir_create(tfZ_distribution_dpath)
    #
    for fn in get_all_files(tfZ_counting_dpath, '', '.pkl'):
        logger.info('Handling %s' % fn)
        _, _, _, _, period = fn[:-len('.pkl')].split('-')
        #
        whole_distribution_fpath = '%s/%s%s.csv' % (tfZ_distribution_dpath, tfZ_distribution_whole_prefix, period)
        if check_path_exist(whole_distribution_fpath):
            logger.info('Already handled %s' % fn)
            continue
        tf_zone_counting_fpath = '%s/%s' % (tfZ_counting_dpath, fn)
        drivers = load_pickle_file(tf_zone_counting_fpath)

        if fn.startswith(tfZ_counting_individuals_prefix):
            distribution = {}
            whole_counting = {}
            for did, tf_zone_counting in drivers.iteritems():
                total_num_trips = sum(tf_zone_counting.values())
                distribution[did] = {}
                for tf_zone, num_trips in tf_zone_counting.iteritems():
                    distribution[did][tf_zone] = num_trips / float(total_num_trips)
                    if not whole_counting.has_key(tf_zone):
                        whole_counting[tf_zone] = 0
                    whole_counting[tf_zone] += num_trips
            distribution_fpath = '%s/%s%s.pkl' % (tfZ_distribution_dpath, tfZ_distribution_individuals_prefix, period)
            save_pickle_file(distribution_fpath, distribution)
            #
            whole_distribution = {}
            year_num_trips = sum(whole_counting.values())
            for tf_zone, tf_zone_counting in whole_counting.iteritems():
                whole_distribution[tf_zone] = tf_zone_counting / float(year_num_trips)
            #
            headers = ['k','timeFrame', 'zid', 'probability']
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
        else:
            assert fn.startswith(tfZ_counting_groups_prefix)
            distribution = {}
            for gn, tf_zone_counting in drivers.iteritems():
                total_num_trips = sum(tf_zone_counting.values())
                distribution[gn] = {}
                for tf_zone, num_trips in tf_zone_counting.iteritems():
                    distribution[gn][tf_zone] = num_trips / float(total_num_trips)
            distribution_fpath = '%s/%s%s.pkl' % (tfZ_distribution_dpath, tfZ_distribution_groups_prefix, period)
            save_pickle_file(distribution_fpath, distribution)


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception tf zone distribution', 'w') as f:
            f.write(format_exc())
        raise