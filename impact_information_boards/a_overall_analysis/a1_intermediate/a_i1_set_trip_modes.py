import __init__  # @UnresolvedImport # @UnusedImport
#
from init_project import taxi_home
from init_project import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from a_overall_analysis.__init__ import trips_dir, trip_prefix  # @UnresolvedImport
from __init__ import IN, OUT  # @UnresolvedImport
from __init__ import ap_poly_fn, ns_poly_fn  # @UnresolvedImport
#
from taxi_common.file_handling_functions import remove_creat_dir  # @UnresolvedImport 
from taxi_common.geo_functions import poly  # @UnresolvedImport
#
import csv
#
def run():
    remove_creat_dir(trips_dir)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                # both years data are corrupted
                continue
            process_files(yymm)

def process_files(yymm):
    yy, mm = yymm[:2], yymm[-2:]
    yyyy = str(2000 + int(yy))
    normal_file = taxi_home + '/%s/%s/trips/trips-%s-normal.csv' % (yyyy, mm, yymm)
    ext_file = taxi_home + '/%s/%s/trips/trips-%s-normal-ext.csv' % (yyyy, mm, yymm)
    #
    # Load data from files
    #
    trip_data1 = read_whole(normal_file)
    trip_data2 = read_whole(ext_file)
    assert len(trip_data1) == len(trip_data2) 
    #
    # Write a combined file
    #
    headers1, headers2 = trip_data1[0], trip_data2[0]
    hid1, hid2 = {h : i for i, h in enumerate(headers1)}, {h : i for i, h in enumerate(headers2)}
    #
    ap_poly, ns_poly = read_generate_polygon(ap_poly_fn), read_generate_polygon(ns_poly_fn)
    vehicle_prev_trip_position_time = {}
    with open('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['tid', 'vid', 'did', 'start-time', 'end-time', 'duration', 'fare', 'ap-trip-mode', 'ns-trip-mode', 'prev-trip-end-time']
        writer.writerow(new_headers)
        for i in range(1, len(trip_data1)):
            row_trip_data1, row_trip_data2 = trip_data1[i], trip_data2[i]
            tid, vid = row_trip_data1[hid1['trip-id']], row_trip_data1[hid1['vehicle-id']]
            st_ts, et_ts = row_trip_data1[hid1['start-time']], row_trip_data1[hid1['end-time']]
            dur, fare = row_trip_data1[hid1['duration']], row_trip_data1[hid1['fare']]
            s_long, s_lat = eval(row_trip_data1[hid1['start-long']]), eval(row_trip_data1[hid1['start-lat']])
            e_long, e_lat = eval(row_trip_data1[hid1['end-long']]), eval(row_trip_data1[hid1['end-lat']])
            c_sl_ap, c_el_ap = ap_poly.is_including((s_long, s_lat)), ap_poly.is_including((e_long, e_lat))
            c_sl_ns, c_el_ns = ns_poly.is_including((s_long, s_lat)), ns_poly.is_including((e_long, e_lat))
            did = row_trip_data2[hid2['driver-id']]
            if not vehicle_prev_trip_position_time.has_key(vid):
                # ASSUMPTION
                # If this trip is the driver's first trip in a month,
                # let's assume that the previous trip occurred at outside of the airport and Night safari
                # and also assume that the previous trip's end time is the current trip's start time
                # False means the trip occur at outside of the airport or Night safari 
                vehicle_prev_trip_position_time[vid] = (OUT, OUT, st_ts)
            pt_el_ap, pt_el_ns, pt_time = vehicle_prev_trip_position_time[vid]
            ap_trip_mode, ns_trip_mode = None, None
            #
            if pt_el_ap == IN and c_sl_ap == IN: ap_trip_mode = DIn_PIn
            elif pt_el_ap == IN and c_sl_ap == OUT: ap_trip_mode = DIn_POut
            elif pt_el_ap == OUT and c_sl_ap == IN: ap_trip_mode = DOut_PIn
            elif pt_el_ap == OUT and c_sl_ap == OUT: ns_trip_mode = DOut_POut   
            else: assert False
            #
            if pt_el_ns == IN and c_sl_ns == IN: ns_trip_mode = DIn_PIn
            elif pt_el_ns == IN and c_sl_ns == OUT: ns_trip_mode = DIn_POut
            elif pt_el_ns == OUT and c_sl_ns == IN: ns_trip_mode = DOut_PIn
            elif pt_el_ns == OUT and c_sl_ns == OUT: ns_trip_mode = DOut_POut   
            else: assert False
            
            new_row = [tid, vid, did,
                       st_ts, et_ts,
                       dur, fare,
                       ap_trip_mode, ns_trip_mode, pt_time]
            writer.writerow(new_row)
            #
            vehicle_prev_trip_position_time[vid] = (c_el_ap, c_el_ns, et_ts)

def read_whole(fn):
    rv = []
    with open(fn, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rv.append(row)
    return rv
            
def read_generate_polygon(fn):
    with open(fn, 'r') as f:
        ls = [w.strip() for w in f.readlines()]
    points = []
    for l in ls:
        _long, _lat = l.split(',')
        points.append([eval(_long), eval(_lat)])
    return poly(points)
    
if __name__ == '__main__':
    run()
