import __init__
#
from community_analysis import all_trip_dir, all_trip_prefix
from community_analysis import year_dist_dir
#
from taxi_common.file_handling_functions import save_pickle_file, check_dir_create
#
import pandas as pd


def run():
    check_dir_create(year_dist_dir)
    #
    year_com_count = {'all': {}}
    for m in range(1, 12):
        yymm = '%02d%02d' % (9, m)
        print 'Handle the file; %s' % yymm
        df = pd.read_csv('%s/%s%s.csv' % (all_trip_dir, all_trip_prefix, yymm))
        for si, sj, num_trips in df.groupby(['si', 'sj']).count().loc[:, ['did']].reset_index().values:
            if si < 0 or sj <0:
                continue
            if not year_com_count['all'].has_key((si, sj)):
                year_com_count['all'][si, sj] = 0
            year_com_count['all'][si, sj] += num_trips
        for cn, si, sj, num_trips in df.groupby(['cn', 'si', 'sj']).count().loc[:, ['did']].reset_index().values:
            if not year_com_count.has_key(cn):
                year_com_count[cn] = {}
                year_com_count[cn][si, sj] = 0
            else:
                if not year_com_count[cn].has_key((si, sj)):
                    year_com_count[cn][si, sj] = 0
            year_com_count[cn][si, sj] += num_trips
    print 'aggregation'
    headers = ['zone', 'prop.']
    LZ, LP = range(2)
    df_data = {k: [] for k in headers}
    for cn in year_com_count.iterkeys():
        sum_count = sum(year_com_count[cn].values())
        for (si, sj), num_trips in year_com_count[cn].iteritems():
            df_data[headers[LZ]].append('z%03d%03d' % (si, sj))
            df_data[headers[LP]].append(num_trips / float(sum_count))
        df = pd.DataFrame(df_data)[headers]
        df.to_csv('%s/%s' % (year_dist_dir, '2009-dist-%s.csv' % cn), index=False)


if __name__ == '__main__':
    run()