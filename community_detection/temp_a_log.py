import __init__
#
from __init__ import taxi_home
from __init__ import logs_dir
from __init__ import FREE, POB
from __init__ import HOUR12
#
from taxi_common.singapore_grid_zone import get_singapore_grid_xy_points
from taxi_common.file_handling_functions import remove_create_dir
#
from bisect import bisect
import csv, datetime
from dateutil.relativedelta import relativedelta


def run():
    process_file('0902')


def process_file(yymm):
    yymm_dir = logs_dir + '/%s' % yymm
    remove_create_dir(yymm_dir)
    def init_processed_file(h_dt):
        processed_fn = yymm_dir + '/%d%02d%02d-%d.csv' % \
                                  (h_dt.year, h_dt.month, h_dt.day, int(h_dt.hour / float(HOUR12)))
        with open(processed_fn, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(['time', 'i', 'j', 'did'])
        return processed_fn
    #
    yy, mm = yymm[:2], yymm[2:]
    fn = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm)
    with open(fn, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        # {'longitude': 3, 'state': 6, 'vehicle-id': 1, 'time': 0, 'latitude': 4, 'speed': 5, 'driver-id': 2}
        hid = {h: i for i, h in enumerate(headers)}
        h_dt = datetime.datetime(2000 + int(yy), int(mm), 1, 0)
        the_last_slot = h_dt + relativedelta(months=1) - datetime.timedelta(hours=HOUR12)
        last_slot_writing = False
        processed_fn = init_processed_file(h_dt)
        drivers_states = {}
        x_points, y_points = get_singapore_grid_xy_points()
        for row in reader:
            did = row[hid['driver-id']]
            if did == '-1':
                continue
            t = eval(row[hid['time']])
            cur_dt = datetime.datetime.fromtimestamp(t)
            if cur_dt < the_last_slot:
                continue
            longitude, latitude = eval(row[hid['longitude']]), eval(row[hid['latitude']])
            state = int(row[hid['state']])
            if not drivers_states.has_key(did): drivers_states[did] = FREE
            prev_state = drivers_states[did]
            if prev_state == FREE and state == POB:
                # Only POB state logs will be recorded
                # Find a cell in grid
                i, j = bisect(x_points, longitude) - 1, bisect(y_points, latitude) - 1
                #
                cur_dt = datetime.datetime.fromtimestamp(t)
                if h_dt + datetime.timedelta(hours=HOUR12) < cur_dt:
                    processed_fn = init_processed_file(h_dt)
                    h_dt = cur_dt
                if not last_slot_writing and the_last_slot < cur_dt:
                    processed_fn = init_processed_file(cur_dt)
                    last_slot_writing = True
                with open(processed_fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([t, i, j, did])
            drivers_states[did] = state
    cur_dt = datetime.datetime.fromtimestamp(t)
    processed_fn = init_processed_file(cur_dt)
    with open(processed_fn, 'a') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow([t, i, j, did])


if __name__ == '__main__':
    run()
