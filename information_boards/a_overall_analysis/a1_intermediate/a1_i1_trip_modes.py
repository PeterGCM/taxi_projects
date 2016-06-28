import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import taxi_home
from __init__ import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from __init__ import ap_poly, ns_poly
from __init__ import IN, OUT
from a_overall_analysis.__init__ import trips_dir, trip_prefix  # @UnresolvedImport
#
from taxi_common.file_handling_functions import remove_creat_dir  # @UnresolvedImport
#
import csv


def run():
    remove_creat_dir(trips_dir)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                # both years data are corrupted
                continue
            process_file(yymm)


def process_file(yymm):
    yy, mm = yymm[:2], yymm[-2:]
    yyyy = str(2000 + int(yy))
    normal_file = taxi_home + '/%s/%s/trips/trips-%s-normal.csv' % (yyyy, mm, yymm)
    ext_file = taxi_home + '/%s/%s/trips/trips-%s-normal-ext.csv' % (yyyy, mm, yymm)
    #
    vehicle_prev_trip_position_time = {}
    with open('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['tid', 'vid', 'did', 'start-time', 'end-time',
                       'duration', 'fare',
                       'ap-trip-mode', 'ns-trip-mode',
                       'prev-trip-end-time']
        writer.writerow(new_headers)
        #
        with open(normal_file, 'rb') as r_csvfile1:
            reader1 = csv.reader(r_csvfile1)
            headers1 = reader1.next()
            # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
            #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
            #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
            #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
            #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}  
            hid1 = {h : i for i, h in enumerate(headers1)}
            with open(ext_file, 'rb') as r_csvfile2:
                reader2 = csv.reader(r_csvfile2)
                headers2 = reader2.next()
                # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
                hid2 = {h : i for i, h in enumerate(headers2)}
                for row1 in reader1:
                    row2 = reader2.next()
                    tid, vid = row1[hid1['trip-id']], row1[hid1['vehicle-id']]
                    st_ts, et_ts = row1[hid1['start-time']], row1[hid1['end-time']]
                    dur, fare = row1[hid1['duration']], row1[hid1['fare']]
                    s_long, s_lat = eval(row1[hid1['start-long']]), eval(row1[hid1['start-lat']])
                    e_long, e_lat = eval(row1[hid1['end-long']]), eval(row1[hid1['end-lat']])
                    c_sl_ap, c_el_ap = ap_poly.is_including((s_long, s_lat)), ap_poly.is_including((e_long, e_lat))
                    c_sl_ns, c_el_ns = ns_poly.is_including((s_long, s_lat)), ns_poly.is_including((e_long, e_lat))
                    did = row2[hid2['driver-id']]
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

if __name__ == '__main__':
    run()
