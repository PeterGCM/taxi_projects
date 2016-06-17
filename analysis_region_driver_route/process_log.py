from __future__ import division
#
from classes import driver
from _setting import zone_driver_prefix
#
import os, pickle
import time, datetime
import csv 
from bisect import bisect  
import sys; sys.setrecursionlimit(150000)
#
x_points, y_points, zones = None, None, None
tf_ts, tt_ts = None, None
log_grid_fn = None
#
POB = 5
RECORDING_INTERVAL = 60 * 10
log_grid_prefix = 'log-grid-'
#
def get_log_grid_file_name(time_from, time_to):
    tf_str = str(time_from[0])[-2:] + ''.join(['%02d' % d for d in time_from[1:]])
    tt_str = str(time_to[0])[-2:] + ''.join(['%02d' % d for d in time_from[1:]])
    return '%s%s-%s.csv' % (log_grid_prefix, tf_str, tt_str)

def run(_x_points, _y_points, _zones, time_from, time_to):
    global x_points, y_points, zones, tf_ts, tt_ts
    x_points, y_points, zones = _x_points, _y_points, _zones
    tf_ts = time.mktime(datetime.datetime(*time_from).timetuple()) 
    tt_ts = time.mktime(datetime.datetime(*time_to).timetuple())
    #
    global log_grid_fn
    log_grid_fn = get_log_grid_file_name(time_from, time_to)
    if not os.path.exists(zone_visual_info_fn):
        save_meaningful_log(x_points, y_points, time_from, time_to)
    #
    out_boundary_logs_fn = 'out_boundary.txt'
    out_boundary_logs_num = 0
    with open(out_boundary_logs_fn, 'w') as f:
        f.write('time,did,i,j,state,zone_defined' + '\n')
    #
    drivers = {}
    init_time = time.time()
    with open(log_grid_fn, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        # {'i': 1, 'did': 3, 'state': 4, 'j': 2, 'time': 0}
        hid = {h : i for i, h in enumerate(headers)}
        print hid
        old_time = time.time()
        for row in reader:
            t = eval(row[hid['time']])
            did = row[hid['did']]
            i, j = int(row[hid['i']]), int(row[hid['j']])
            state = int(row[hid['state']])
            #
            # Find a targeted zone
            #
            try:
                z = zones[(i, j)]
                #
                try:
                    assert z.check_validation()
                except AssertionError:
                    out_boundary_logs_num += 1
                    with open(out_boundary_logs_fn, 'a') as f:
                        f.write('%d,%s,%d,%d,%d,O' % (t, did, i, j, state) + '\n')
                    continue
            except KeyError:
                out_boundary_logs_num += 1
                with open(out_boundary_logs_fn, 'a') as f:
                    f.write('%d,%s,%d,%d,%d,X' % (t, did, i, j, state) + '\n')
                continue
            #
            if not drivers.has_key(did): drivers[did] = driver(did)
            d = drivers[did]
            if state == POB:
                d.update_relation(t, z)
            else:
                d.update_position(t, z)
            if time.time() - old_time > RECORDING_INTERVAL:
                save_pkl_file(t, zones, drivers)
                old_time = time.time()
    save_pkl_file(tt_ts, zones, drivers)

def save_meaningful_log(x_points, y_points, time_from, time_to):
    csv_files = get_csv_files(time_from, time_to)
    drivers = {}
    log_grid_fn = get_log_grid_file_name(time_from, time_to) 
    with open(log_grid_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['time', 'i', 'j', 'did', 'state'])
    #
    for fn in csv_files:
        with open(fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            # {'longitude': 3, 'state': 6, 'vehicle-id': 1, 'time': 0, 'latitude': 4, 'speed': 5, 'driver-id': 2}
            hid = {h : i for i, h in enumerate(headers)}
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
                # Find a cell in grid
                #
                i, j = bisect(x_points, longitude) - 1, bisect(y_points, latitude) - 1
                #
                if not drivers.has_key(did): drivers[did] = (None, None)
                i0, j0 = drivers[did]
                if state == POB or not (i0 == i or j0 == j):
                    with open(log_grid_fn, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        writer.writerow([t, i, j, did, state])

def save_pkl_file(t, zones, drivers):
    _, _, tf, _ = log_grid_fn[:-len('.csv')].split('-')
    #
    t_dt = datetime.datetime.fromtimestamp(t)
    t_str = str(t_dt.year)[-2:] + \
         ''.join(['%02d' % d for d in [t_dt.month, t_dt.day, t_dt.hour, t_dt.minute, t_dt.second]])
    with open('%s%s-%s.pkl' % (zone_driver_prefix, tf, t_str), 'wb') as fp:
        pickle.dump([(d.did, d.relation) for d in drivers], fp)
    
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
