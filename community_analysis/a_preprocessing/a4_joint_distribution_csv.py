import __init__
#
from community_analysis import tf_zone_counting_dir, tf_zone_counting_prefix
from community_analysis import tf_zone_distribution_dir, tf_zone_distribution_prefix
from community_analysis import PM2, PM11
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, check_dir_create
from taxi_common.sg_grid_zone import get_sg_zones
#
import pandas as pd


def run():
    check_dir_create(tf_zone_distribution_dir)
    #
    for year_dist_pkl_fn in get_all_files(tf_zone_counting_dir, '', '.pkl'):
        _, _, _, yyyy = year_dist_pkl_fn[:-len('.pkl')].split('-')
        if not yyyy.startswith('20'):
            continue
        print 'handling %s' % yyyy
        #
        year_counting = load_pickle_file('%s/%s%s.pkl' % (tf_zone_counting_dir, tf_zone_counting_prefix, yyyy))
        year_count_aggregation = {}
        for did, counting in year_counting.iteritems():
            for tf_zone, num_trips in counting.iteritems():
                if not year_count_aggregation.has_key(tf_zone):
                    year_count_aggregation[tf_zone] = 0
                year_count_aggregation[tf_zone] += num_trips
        #
        year_dist = {}
        year_num_trips = sum(year_count_aggregation.values())
        for tf_zone, tf_zone_counting in year_count_aggregation.iteritems():
            year_dist[tf_zone] = tf_zone_counting / float(year_num_trips)
        #
        year_dist_csv_fpath = '%s/%s%s.csv' % (tf_zone_distribution_dir, tf_zone_distribution_prefix, yyyy)
        headers = ['timeFrame', 'zid', 'probability']
        LTF, LZ, LP = range(3)
        zones = get_sg_zones()
        df_data = {k: [] for k in headers}
        for tf in range(PM2, PM11 + 1):
            for (i, j) in zones.iterkeys():
                if i < 0 or j < 0:
                    continue
                k = (tf, i, j)
                prob = year_dist[k] if year_dist.has_key(k) else 0
                df_data[headers[LTF]].append(tf)
                df_data[headers[LZ]].append('z%03d%03d' % (i, j))
                df_data[headers[LP]].append(prob)
        df = pd.DataFrame(df_data)[headers]
        df.to_csv(year_dist_csv_fpath, index=False)


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception tf zone csv.txt', 'w') as f:
            f.write(format_exc())
        raise