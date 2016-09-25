import __init__
#
from community_analysis import all_trip_dir, all_trip_prefix
from community_analysis import year_dist_dir
from community_analysis import PM2, PM11
#
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.sg_grid_zone import get_sg_zones
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
        for hh, si, sj, num_trips in df.groupby(['hh', 'si', 'sj']).count().loc[:, ['did']].reset_index().values:
            if si < 0 or sj <0:
                continue
            if not year_com_count['all'].has_key((hh, si, sj)):
                year_com_count['all'][hh, si, sj] = 0
            year_com_count['all'][hh, si, sj] += num_trips
        for cn, hh, si, sj, num_trips in df.groupby(['cn', 'hh', 'si', 'sj']).count().loc[:, ['did']].reset_index().values:
            if not year_com_count.has_key(cn):
                year_com_count[cn] = {}
                year_com_count[cn][hh, si, sj] = 0
            else:
                if not year_com_count[cn].has_key((hh, si, sj)):
                    year_com_count[cn][hh, si, sj] = 0
            year_com_count[cn][hh, si, sj] += num_trips
    print 'aggregation'
    headers = ['time-frame', 'zone', 'num-trips']
    LTF, LZ, LP = range(3)
    df_data = {k: [] for k in headers}
    zones = get_sg_zones()
    for cn, year_counting in year_com_count.iteritems():
        for tf in range(PM2, PM11 + 1):
            for (i, j) in zones.iterkeys():
                if i < 0 or j < 0:
                    continue
                k = (tf, i, j)
                num_trips = year_counting[k] if year_counting.has_key(k) else 0
                df_data[headers[LTF]].append(tf)
                df_data[headers[LZ]].append('z%03d%03d' % (i, j))
                df_data[headers[LP]].append(num_trips)
        df = pd.DataFrame(df_data)[headers]
        df.to_csv('%s/%s' % (year_dist_dir, '2009-trip-counting-%s.csv' % cn), index=False)


if __name__ == '__main__':
    run()