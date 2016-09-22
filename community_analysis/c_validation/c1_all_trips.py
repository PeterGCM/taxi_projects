import __init__
#
from community_analysis.c_validation import top5_com_TH92_fpath
from community_analysis import FRI, SAT, SUN
from community_analysis import PM2, PM11
from community_analysis import taxi_home, all_trip_dir, all_trip_prefix
#
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common import full_time_driver_dir, ft_drivers_prefix
#
from bisect import bisect
import csv, datetime


def run():
    check_dir_create(all_trip_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for mm in range(1, 12):
        yymm = '09%02d' % mm
        # process_file(yymm)
        put_task(process_file, [yymm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'Handle the file; %s' % yymm
    processed_fpath = '%s/%s%s.csv' % (all_trip_dir, all_trip_prefix, yymm)
    with open(processed_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['time', 'did', 'cn',
                         'start-long', 'start-lat', 'end-long', 'end-lat',
                         'distance', 'duration', 'fare',
                         'si', 'sj', 'ei', 'ej'])
    #
    ft_drivers = load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm))
    #
    top5_com_drivers = load_pickle_file(top5_com_TH92_fpath)
    did_cn = {}
    for cn, com_drivers in top5_com_drivers.iteritems():
        for did in com_drivers:
            did_cn[did] = cn
    #
    x_points, y_points = get_sg_grid_xy_points()
    yy, mm = yymm[:2], yymm[2:]
    normal_fpath = '%s/20%s/%s/trips/trips-%s-normal.csv' % (taxi_home, yy, mm, yymm)
    ext_fpath = '%s/20%s/%s/trips/trips-%s-normal-ext.csv' % (taxi_home, yy, mm, yymm)

    with open(normal_fpath, 'rb') as r_csvfile1:
        reader1 = csv.reader(r_csvfile1)
        headers1 = reader1.next()
        # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
        #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
        #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
        #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
        #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}
        hid1 = {h: i for i, h in enumerate(headers1)}
        with open(ext_fpath, 'rb') as r_csvfile2:
            reader2 = csv.reader(r_csvfile2)
            headers2 = reader2.next()
            # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
            hid2 = {h: i for i, h in enumerate(headers2)}
            #
            h_dt = datetime.datetime(2000 + int(yy), int(mm), 1, 0)
            for row1 in reader1:
                row2 = reader2.next()
                did = row2[hid2['driver-id']]
                if did == '-1':
                    continue
                #
                if did not in ft_drivers:
                    continue
                t = eval(row1[hid1['start-time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                if cur_dt.weekday() in [FRI, SAT, SUN]:
                    continue
                if cur_dt.hour < PM2:
                    continue
                if PM11 < cur_dt.hour:
                    continue
                #
                s_long, s_lat = eval(row1[hid1['start-long']]), eval(row1[hid1['start-lat']])
                e_long, e_lat = eval(row1[hid1['end-long']]), eval(row1[hid1['end-lat']])
                si, sj = bisect(x_points, s_long) - 1, bisect(y_points, s_lat) - 1
                ei, ej = bisect(x_points, e_long) - 1, bisect(y_points, e_lat) - 1
                #
                cn = did_cn[int(did)] if did_cn.has_key(int(did)) else 'None'
                with open(processed_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([t, did, cn,
                                     s_long, s_lat, e_long, e_lat,
                                     row1[hid1['distance']], row1[hid1['duration']], row1[hid1['fare']],
                                     si, sj, ei, ej])
    print 'End the file; %s' % yymm

if __name__ == '__main__':
    run()