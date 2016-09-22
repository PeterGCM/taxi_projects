import __init__
#
from community_analysis import all_trip_dir, all_trip_prefix
from community_analysis import year_dist_dir, year_dist_fpath
#
from taxi_common.file_handling_functions import save_pickle_file, check_dir_create
#
import pandas as pd


def run():
    check_dir_create(year_dist_dir)
    #
    year_com_count = {}
    for m in range(1, 12):
        yymm = '%02d%02d' % (9, m)
        print 'Handle the file; %s' % yymm
        df = pd.read_csv('%s/%s%s.csv' % (all_trip_dir, all_trip_prefix, yymm))
        for cn, si, sj, v in df.groupby(['cn', 'si', 'sj']).count().loc[:, ['did']].reset_index().values:
            if not year_com_count.has_key(cn):
                year_com_count[cn] = {}
                year_com_count[cn][si, sj] = 0
            else:
                if not year_com_count[cn].has_key((si, sj)):
                    year_com_count[cn][si, sj] = 0
            year_com_count[cn][si, sj] += v
    print 'aggregation'
    year_com_dist = {}
    for cn in year_com_count.iterkeys():
        year_com_dist[cn] = {}
        sum_count = sum(year_com_count[cn].values())
        for (si, sj), num_trips in year_com_count[cn].iteritems():
            year_com_dist[cn][si, sj] = num_trips / float(sum_count)
    save_pickle_file(year_dist_fpath, year_com_dist)


if __name__ == '__main__':
    run()