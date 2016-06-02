from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import taxi_home
from supports._setting import trips_dir, trip_prefix
#
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports._setting import DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS
from supports._setting import IN_NS, OUT_NS
from supports.etc_functions import remove_creat_dir
from supports.location_check import check_terminal_num, is_in_night_safari
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

def read_whole(fn):
    rv = []
    with open(fn, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rv.append(row)
    return rv

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
            c_start_ter, c_end_ter = check_terminal_num(s_long, s_lat), check_terminal_num(e_long, e_lat)
            c_sl_ns, c_el_ns = is_in_night_safari(s_long, s_lat), is_in_night_safari(e_long, e_lat)
            did = row_trip_data2[hid2['driver-id']]
            if not vehicle_prev_trip_position_time.has_key(vid):
                # ASSUMPTION
                # If this trip is the driver's first trip in a month,
                # let's assume that the previous trip occurred out of the airport and out of the night safari
                # and also assume that the previous trip's end time is the current trip's start time 
                # -1 represents out of airport zone
                vehicle_prev_trip_position_time[vid] = (-1, OUT_NS, st_ts)
            prev_trip_end_ter, prev_trip_end_loc_ns, prev_trip_time = vehicle_prev_trip_position_time[vid]
            ap_trip_mode, ns_trip_mode = None, None
            if prev_trip_end_ter != -1 and c_start_ter != -1 : ap_trip_mode = DInAP_PInAP
            elif prev_trip_end_ter != -1 and c_start_ter == -1: ap_trip_mode = DInAP_POutAP
            elif prev_trip_end_ter == -1 and c_start_ter != -1: ap_trip_mode = DOutAP_PInAP
            elif prev_trip_end_ter == -1 and c_start_ter == -1: ap_trip_mode = DOutAP_POutAP
            else: assert False
            #
            if prev_trip_end_loc_ns == IN_NS and c_sl_ns == IN_NS: ns_trip_mode = DInNS_PInNS
            elif prev_trip_end_loc_ns == IN_NS and c_sl_ns == OUT_NS: ns_trip_mode = DInNS_POutNS
            elif prev_trip_end_loc_ns == OUT_NS and c_sl_ns == IN_NS: ns_trip_mode = DOutNS_PInNS
            elif prev_trip_end_loc_ns == OUT_NS and c_sl_ns == OUT_NS: ns_trip_mode = DOutNS_POutNS   
            else: assert False
            
            new_row = [tid, vid, did,
                       st_ts, et_ts,
                       dur, fare,
                       ap_trip_mode, ns_trip_mode, prev_trip_time]
            writer.writerow(new_row)
            #
            vehicle_prev_trip_position_time[vid] = (c_end_ter, c_el_ns, et_ts)
            
if __name__ == '__main__':
    run()
