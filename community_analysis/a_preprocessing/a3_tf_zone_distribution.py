import __init__
#
from community_analysis import tf_zone_counting_dir, tf_zone_counting_prefix
from community_analysis import tf_zone_distribution_dir, tf_zone_distribution_prefix
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, load_pickle_file, save_pickle_file, save_pkl_threading


def run():
    check_dir_create(tf_zone_distribution_dir)
    #
    for y in range(10, 12):
        yyyy = '20%02d' % y
        print 'Handle %s' % yyyy
        year_distribution_fpath = '%s/%s%s.pkl' % (tf_zone_distribution_dir, tf_zone_distribution_prefix, yyyy)
        if check_path_exist(year_distribution_fpath):
            continue
        year_counting_fpath = '%s/%s%s.pkl' % (tf_zone_counting_dir, tf_zone_counting_prefix, yyyy)
        if check_path_exist(year_counting_fpath):
            year_counting = load_pickle_file(year_counting_fpath)
        else:
            year_counting = {}
            for m in range(1, 13):
                yymm = '%02d%02d' % (y, m)
                print 'Handle the file; %s' % yymm
                tf_zone_counting_fpath = '%s/%s%s.pkl' % (tf_zone_counting_dir, tf_zone_counting_prefix, yymm)
                if not check_path_exist(tf_zone_counting_fpath):
                    print 'The file X exists; %s' % yymm
                    continue
                drivers = load_pickle_file(tf_zone_counting_fpath)
                for did, tf_zone_counting in drivers.iteritems():
                    if not year_counting.has_key(did):
                        year_counting[did] = {}
                    for tf_zone, num_trips in tf_zone_counting.iteritems():
                        if not year_counting[did].has_key(tf_zone):
                            year_counting[did][tf_zone] = 0
                        year_counting[did][tf_zone] += num_trips
            save_pkl_threading(year_counting_fpath, year_counting)
        year_dist = {}
        for did, tf_zone_counting in year_counting.iteritems():
            year_num_trips = sum(tf_zone_counting.values())
            year_dist[did] = {}
            for tf_zone, num_trips in tf_zone_counting.iteritems():
                year_dist[did][tf_zone] = num_trips / float(year_num_trips)
        save_pickle_file(year_distribution_fpath, year_dist)


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception tf zone distribution.txt', 'w') as f:
            f.write(format_exc())
        raise