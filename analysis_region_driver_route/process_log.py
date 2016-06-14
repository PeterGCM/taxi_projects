from __future__ import division

from bisect import bisect, bisect_right
import csv

x_points, y_points, zones = None, None, None

def run(_x_points, _y_points, _zones, time_from, time_to):
    global x_points, y_points, zones
    x_points, y_points, zones = _x_points, _y_points, _zones 
    #
    tf_year, tf_month, tf_day, tf_hour, tf_minute, tf_second = time_from  
    tt_year, tt_month, tt_day, tt_hour, tt_minute, tt_second = time_to
    # TODO
    # Set timestamp and ignore logs which does not belong to the period
    tf_ts = None
    tt_ts = None
    
    csv_files = get_csv_files(time_from, time_to)
    for fn in csv_files:
        with open(fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            # {'longitude': 3, 'state': 6, 'vehicle-id': 1, 'time': 0, 'latitude': 4, 'speed': 5, 'driver-id': 2}
            for row in reader:
                ts = row[hid['driver-id']]
                longitude, latitude = eval(row[hid['longitude']]), eval(row[hid['latitude']])
                z = get_zone(longitude, latitude)
                state = row[hid['state']]
                
                
                assert False

def get_zone(longitude, latitude):
    i = bisect(x_points, longitude) - 1
    j = bisect(y_points, latitude) - 1
    print i, j
    z = zones[(i, j)]
    assert z.check_validation()
    #
    return zones[(i, j)]
    
def get_csv_files(time_from, time_to):
    #
    # TODO
    #
    return ['logs-0901-normal.csv']

if __name__ == '__main__':
    from _setting import zone_visual_info_fn
    import pickle
    with open(zone_visual_info_fn, 'rb') as fp:
        x_points, y_points, zones, singapore_poly_points, lines = pickle.load(fp)
    run(x_points, y_points, zones, (2009, 1, 1, 0, 5, 30), (2009, 1, 1, 0, 10, 30))
