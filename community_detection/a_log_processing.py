import __init__
#
from __init__ import taxi_home, grid_info_fn
from __init__ import logs_dir
from __init__ import ZONE_UNIT_KM
from __init__ import FREE, POB
from __init__ import HOUR12
from _classes import cd_zone
#
from taxi_common.file_handling_functions import check_path_exist, save_pickle_file, load_pickle_file, remove_create_dir
#
from bisect import bisect
import csv, datetime

x_points, y_points = None, None

def run():
    global x_points, y_points, zones
    if not check_path_exist(grid_info_fn):
        from taxi_common.split_into_zones import run as run_split_into_zones
        x_points, y_points, _ = run_split_into_zones(ZONE_UNIT_KM, cd_zone)
        save_pickle_file(grid_info_fn, [x_points, y_points, zones])
    else:
        x_points, y_points, _ = load_pickle_file(grid_info_fn)
    #
    process_file('0901')


def process_file(yymm):
    yymm_dir = logs_dir + '/' + yymm
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
        processed_fn = init_processed_file(h_dt)
        drivers_states = {}
        for row in reader:
            did = row[hid['driver-id']]
            if did == '-1':
                continue
            t = eval(row[hid['time']])
            longitude, latitude = eval(row[hid['longitude']]), eval(row[hid['latitude']])
            state = int(row[hid['state']])
            if not drivers_states.has_key(did): drivers_states[did] = FREE
            prev_state = drivers_states[did]
            if prev_state == FREE and state == POB:
                # Only POB state logs will be recorded
                # Find a cell in grid
                i, j = bisect(x_points, longitude) - 1, bisect(y_points, latitude) - 1
                #
                cur_time = datetime.datetime.fromtimestamp(t)
                if h_dt + datetime.timedelta(hours=HOUR12) < cur_time:
                    processed_fn = init_processed_file(h_dt)
                    h_dt = cur_time
                with open(processed_fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([t, i, j, did])
            drivers_states[did] = state


if __name__ == '__main__':
    run()
