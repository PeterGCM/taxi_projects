from __init__ import get_processed_log_fn, get_timeslot
#
from classes import rp_driver
#
from bisect import bisect
import csv, datetime, time

def run(x_points, y_points, time_from, time_to):
    tf_ts = time.mktime(datetime.datetime(*time_from).timetuple()) 
    tt_ts = time.mktime(datetime.datetime(*time_to).timetuple())
    #
    csv_files = get_csv_files(time_from, time_to)
    drivers = {}
    processed_log_fn = get_processed_log_fn(time_from, time_to)
    with open(processed_log_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['time', 'did', 'state', 'i', 'j', 'timeslot', 'state-duration'])
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
                    if not drivers.has_key(did): drivers[did] = rp_driver(did)
                    d = drivers[did]
                    state_duration = d.last_log_time - t if d.last_log_time else 0
                    timeslot = get_timeslot(tf_ts, t)
                    writer.writerow([t, did, state, i, j, timeslot, state_duration])

def get_csv_files(time_from, time_to):
    #
    # TODO
    #
    return ['logs-0901-normal.csv']
