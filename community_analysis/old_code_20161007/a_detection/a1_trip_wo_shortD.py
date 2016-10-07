import __init__
#
from community_analysis.a_detection import KM2
from community_analysis import FRI, SAT, SUN
from community_analysis import PM2, PM11
from community_analysis import taxi_home, trip_dir
#
from taxi_common.file_handling_functions import remove_create_dir, load_pickle_file, check_dir_create
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common import full_time_driver_dir, ft_drivers_prefix
#
from bisect import bisect
import csv, datetime


def run():
    check_dir_create(trip_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for mm in range(1, 10):
        # yymm = '09%02d' % mm
        yymm = '12%02d' % mm
        # process_file(yymm)
        put_task(process_file, [yymm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'handle the file; %s' % yymm
    ft_drivers = load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm))
    yymm_dir = trip_dir + '/%s' % yymm
    remove_create_dir(yymm_dir)
    def init_processed_file(h_dt):
        processed_fn = yymm_dir + '/%d%02d%02d.csv' % \
                                  (h_dt.year, h_dt.month, h_dt.day)
        with open(processed_fn, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['time', 'did',
                             'start-long', 'start-lat', 'end-long', 'end-lat',
                             'distance', 'duration', 'fare',
                             'si', 'sj', 'ei', 'ej'])
        return processed_fn
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
            processed_fn = init_processed_file(h_dt)
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
                dist = eval(row1[hid1['distance']])
                if dist < KM2:
                    continue
                #
                s_long, s_lat = eval(row1[hid1['start-long']]), eval(row1[hid1['start-lat']])
                e_long, e_lat = eval(row1[hid1['end-long']]), eval(row1[hid1['end-lat']])
                si, sj = bisect(x_points, s_long) - 1, bisect(y_points, s_lat) - 1
                ei, ej = bisect(x_points, e_long) - 1, bisect(y_points, e_lat) - 1
                #
                if h_dt.day < cur_dt.day:
                    processed_fn = init_processed_file(h_dt)
                    h_dt = cur_dt
                    print cur_dt
                with open(processed_fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([t, did,
                                     s_long, s_lat, e_long, e_lat,
                                     dist, row1[hid1['duration']], row1[hid1['fare']],
                                     si, sj, ei, ej])


if __name__ == '__main__':
    run()
