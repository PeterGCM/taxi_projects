from __future__ import division
#
from classes import driver
from _setting import zone_driver_prefix
#
from bisect import bisect
import csv
import pickle
import time, datetime 
import sys

sys.setrecursionlimit(150000)

POB = 5

x_points, y_points, zones = None, None, None

RECORDING_INTERVAL = 60 * 5

def run(_x_points, _y_points, _zones, time_from, time_to):
    out_boundary_logs_fn = 'out_boundary.txt'
    out_boundary_logs_num = 0
    
    with open(out_boundary_logs_fn, 'w') as f:
        f.write('time,driver-id,longitude,latitude,state,zone_defined' + '\n')
    
    
    init_time = time.time()
    global x_points, y_points, zones
    x_points, y_points, zones = _x_points, _y_points, _zones
    #
    tf_str = str(time_from[0])[-2:] + ''.join(['%02d' % d for d in time_from[1:]])
    tt_str = str(time_to[0])[-2:] + ''.join(['%02d' % d for d in time_from[1:]])
    tf_ts = time.mktime(datetime.datetime(*time_from).timetuple())
    tt_ts = time.mktime(datetime.datetime(*time_to).timetuple())
    #
    csv_files = get_csv_files(time_from, time_to)
    drivers = {}
    for fn in csv_files:
        with open(fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            # {'longitude': 3, 'state': 6, 'vehicle-id': 1, 'time': 0, 'latitude': 4, 'speed': 5, 'driver-id': 2}
            hid = {h : i for i, h in enumerate(headers)}
            old_time = time.time()
            for row in reader:
                t = eval(row[hid['time']])
                if t < tf_ts:
                    continue
                if t > tt_ts:
                    break
                did = row[hid['driver-id']]
                longitude, latitude = eval(row[hid['longitude']]), eval(row[hid['latitude']])
                state = int(row[hid['state']])
                #
                # Find a targeted zone
                #
                i = bisect(x_points, longitude) - 1
                j = bisect(y_points, latitude) - 1
                try:
                    z = zones[(i, j)]
                    #
                    try:
                        assert z.check_validation()
                    except AssertionError:
                        out_boundary_logs_num += 1
                        with open(out_boundary_logs_fn, 'a') as f:
                            f.write('%d,%s,%f,%f,%d,O' % (t, did, longitude, latitude, state) + '\n')
                        continue
                except KeyError:
                    out_boundary_logs_num += 1
                    with open(out_boundary_logs_fn, 'a') as f:
                        f.write('%d,%s,%f,%f,%d,X' % (t, did, longitude, latitude, state) + '\n')
                    continue
                #
                z = get_zone(longitude, latitude)
                #
                if not drivers.has_key(did): drivers[did] = driver(did)
                d = drivers[did]
                if state == POB:
                    z.update_Q(t)
                    d.update_relation(z)
                else:
                    d.update_position(t, z)
                if time.time() - old_time > RECORDING_INTERVAL:
                    t_dt = datetime.datetime.fromtimestamp(t)
                    t_str = str(t_dt.year)[-2:] + \
                         ''.join(['%02d' % d for d in [t_dt.month, t_dt.day, t_dt.hour, t_dt.minute, t_dt.second]])
                    with open('%s%s-%s.pkl' % (zone_driver_prefix, tf_str, t_str), 'wb') as fp:
                        pickle.dump([time.time() - init_time, zones, drivers], fp)
                    old_time = time.time()
    with open('%s%s-%s.pkl' % (zone_driver_prefix, tf_str, tt_str), 'wb') as fp:
        pickle.dump([time.time() - init_time, zones, drivers], fp)
                 

def get_zone(longitude, latitude):
    i = bisect(x_points, longitude) - 1
    j = bisect(y_points, latitude) - 1
    z = zones[(i, j)]
    #
    try:
        assert z.check_validation()
    except AssertionError:
        pass
    #
    return zones[(i, j)]
    
def get_csv_files(time_from, time_to):
    #
    # TODO
    #
    return ['logs-0901-normal.csv']

if __name__ == '__main__':
    from _setting import zone_visual_info_fn
    with open(zone_visual_info_fn, 'rb') as fp:
        x_points, y_points, zones, singapore_poly_points, lines = pickle.load(fp)
    run(x_points, y_points, zones, (2009, 1, 1, 0, 0, 30), (2009, 1, 1, 1, 0, 30))
