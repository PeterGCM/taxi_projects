import __init__
#
from __init__ import whole_trip_prefix
from community_analysis.__init__ import FRI, SAT, SUN
from community_analysis.__init__ import PM2, PM3
from community_analysis.__init__ import taxi_home, trips_dir
#
from taxi_common.file_handling_functions import remove_create_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime


def run():
    global yyyy_dir
    yyyy_dir = trips_dir + '/%s' % 2009; remove_create_dir(yyyy_dir)
    init_multiprocessor(11)
    count_num_jobs = 0
    for mm in range(1, 12):
        put_task(process_file, ['09%02d' % mm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'handle the file; %s' % yymm
    yy, mm = yymm[:2], yymm[-2:]
    yyyy = str(2000 + int(yy))
    normal_file = taxi_home + '/%s/%s/trips/trips-%s-normal.csv' % (yyyy, mm, yymm)
    ext_file = taxi_home + '/%s/%s/trips/trips-%s-normal-ext.csv' % (yyyy, mm, yymm)
    fn = '%s/%s%s.csv' % (yyyy_dir, whole_trip_prefix, yymm)
    with open(fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['did',
                       'start-time', 'end-time',
                       'start-long', 'start-lat',
                       'end-long', 'end-lat',
                       'duration', 'fare']
        writer.writerow(new_headers)
        #
    with open(normal_file, 'rb') as r_csvfile1:
        reader1 = csv.reader(r_csvfile1)
        headers1 = reader1.next()
        # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
        #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
        #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
        #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
        #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}
        hid1 = {h : i for i, h in enumerate(headers1)}
        with open(ext_file, 'rb') as r_csvfile2:
            reader2 = csv.reader(r_csvfile2)
            headers2 = reader2.next()
            # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
            hid2 = {h : i for i, h in enumerate(headers2)}
            for row1 in reader1:
                row2 = reader2.next()
                #
                did = row2[hid2['driver-id']]
                if did == '-1':
                    continue
                #
                st_ts, et_ts = row1[hid1['start-time']], row1[hid1['end-time']]
                t = eval(st_ts)
                cur_dt = datetime.datetime.fromtimestamp(t)
                if cur_dt.weekday() in [FRI, SAT, SUN]:
                    continue
                if cur_dt.hour < PM2:
                    continue
                if PM3 < cur_dt.hour:
                    continue
                #
                with open(fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([did,
                                     st_ts, et_ts,
                                     row1[hid1['start-long']], row1[hid1['start-lat']],
                                     row1[hid1['end-long']], row1[hid1['end-lat']],
                                     row1[hid1['duration']], row1[hid1['fare']]])


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise