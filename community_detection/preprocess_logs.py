from __init__ import get_processed_log_fn
from __init__ import POB

from bisect import bisect
import csv, datetime, time

def run(x_points, y_points, time_from, time_to):
    tf_ts = time.mktime(datetime.datetime(*time_from).timetuple()) 
    tt_ts = time.mktime(datetime.datetime(*time_to).timetuple())
    #
    csv_files = get_csv_files(time_from, time_to)
    drivers = {}
    log_grid_fn = get_processed_log_fn(time_from, time_to)
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
                        
def get_csv_files(time_from, time_to):
    #
    # TODO
    #
    return ['logs-0901-normal.csv']
