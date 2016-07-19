import __init__
#
from __init__ import taxi_home, logs_dir
from __init__ import FREE, HOUR1
#
from taxi_common.singapore_grid_zone import get_singapore_grid_xy_points
from taxi_common.file_handling_functions import remove_create_dir
#
from bisect import bisect
import csv, datetime
from dateutil.relativedelta import relativedelta


def run():
    process_files('0901')


def process_files(yymm):
    yymm_logs_dir = logs_dir + '/%s' % yymm
    remove_create_dir(yymm_logs_dir)
    def init_processed_file(h_dt):
        processed_fn = yymm_logs_dir + '/%d%02d%02d-%d.csv' % \
                                  (h_dt.year, h_dt.month, h_dt.day, int(h_dt.hour / float(HOUR1)))
        with open(processed_fn, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(['time', 'i', 'j', 'did', 'FREE-dur'])
        return processed_fn

    yy, mm = yymm[:2], yymm[2:]
    fn = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm)

    with open(fn, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        # {'longitude': 3, 'state': 6, 'vehicle-id': 1, 'time': 0, 'latitude': 4, 'speed': 5, 'driver-id': 2}
        hid = {h: i for i, h in enumerate(headers)}
        h_dt = datetime.datetime(2000 + int(yy), int(mm), 1, 0)
        the_last_slot = h_dt + relativedelta(months=1) - datetime.timedelta(hours=HOUR1)
        last_slot_writing = False
        processed_fn = init_processed_file(h_dt)
        drivers_lts = {} # drivers the last logging time stame
        x_points, y_points = get_singapore_grid_xy_points()
        for row in reader:
            did = row[hid['driver-id']]
            if did == '-1':
                continue
            t = eval(row[hid['time']])
            longitude, latitude = eval(row[hid['longitude']]), eval(row[hid['latitude']])
            state = int(row[hid['state']])
            if not drivers_lts.has_key(did): drivers_lts[did] = t
            state_duration = t - drivers_lts[did]
            if state == FREE:
                i, j = bisect(x_points, longitude) - 1, bisect(y_points, latitude) - 1
                cur_dt = datetime.datetime.fromtimestamp(t)
                if h_dt + datetime.timedelta(hours=HOUR1) < cur_dt:
                    processed_fn = init_processed_file(h_dt)
                    h_dt = cur_dt
                if not last_slot_writing and the_last_slot < cur_dt:
                    processed_fn = init_processed_file(cur_dt)
                    last_slot_writing = True
                with open(processed_fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([t, i, j, did, state_duration])
            drivers_lts[did] = t


if __name__ == '__main__':
    run()
