import __init__
#
'''

'''
#
from information_boards import taxi_home
from information_boards import trip_dpath, trip_prefix
from information_boards import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from information_boards import IN, OUT
from information_boards import AM2, AM5
from information_boards import error_hours
#
from taxi_common.geo_functions import get_ap_polygons, get_ns_polygon
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv

logger = get_logger()


def run():
    check_dir_create(trip_dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data are corrupted
                continue
            # process_month(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        trip_fpath = '%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm)
        trip_filtered_fpath = '%s/Filtered-%s%s.csv' % (trip_dpath, trip_prefix, yymm)
        if check_path_exist(trip_fpath):
            logger.info('The file had already been processed; %s' % trip_fpath)
            return
        for fpath in [trip_fpath, trip_filtered_fpath]:
            with open(fpath, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_headers = ['vid', 'did',
                               'startTime', 'endTime', 'duration', 'fare',
                               'tripModeAP', 'tripModeNS', 'prevTripEndTime',
                               'year', 'month', 'day', 'hour',
                               'pickUpTerminalAP', 'prevEndTerminalAP']
                writer.writerow(new_headers)
        yy, mm = yymm[:2], yymm[-2:]
        yyyy = str(2000 + int(yy))
        normal_file = taxi_home + '/%s/%s/trips/trips-%s-normal.csv' % (yyyy, mm, yymm)
        ext_file = taxi_home + '/%s/%s/trips/trips-%s-normal-ext.csv' % (yyyy, mm, yymm)
        #
        year, month = int(yyyy), int(mm)
        ap_polygons, ns_polygon = get_ap_polygons(), get_ns_polygon()
        vehicle_prev_trip_position_time = {}
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
                    #
                    vid = row1[hid1['vehicle-id']]
                    st_ts, et_ts = row1[hid1['start-time']], row1[hid1['end-time']]
                    dur, fare = row1[hid1['duration']], row1[hid1['fare']]
                    day, hour = int(row1[hid1['start-day']]), int(row1[hid1['start-hour']])
                    s_long, s_lat = eval(row1[hid1['start-long']]), eval(row1[hid1['start-lat']])
                    e_long, e_lat = eval(row1[hid1['end-long']]), eval(row1[hid1['end-lat']])

                    c_sl_ap, c_el_ap = False, False
                    c_sl_ter, c_el_ter = 'X', 'X'
                    for ap_polygon in ap_polygons:
                        if not c_sl_ap:
                            res = ap_polygon.is_including((s_long, s_lat))
                            if res:
                                c_sl_ap = res
                                c_sl_ter = ap_polygon.name
                        if not c_el_ap:
                            res = ap_polygon.is_including((e_long, e_lat))
                            if res:
                                c_el_ap = res
                                c_el_ter = ap_polygon.name
                    c_sl_ns, c_el_ns = ns_polygon.is_including((s_long, s_lat)), ns_polygon.is_including((e_long, e_lat))
                    did = row2[hid2['driver-id']]
                    #
                    if not vehicle_prev_trip_position_time.has_key(vid):
                        # ASSUMPTION
                        # If this trip is the driver's first trip in a month,
                        # let's assume that the previous trip occurred at outside of the airport and Night safari
                        # and also assume that the previous trip's end time is the current trip's start time
                        # False means the trip occur at outside of the airport or Night safari
                        vehicle_prev_trip_position_time[vid] = ('X', OUT, OUT, st_ts)
                    pt_el_ter, pt_el_ap, pt_el_ns, pt_time = vehicle_prev_trip_position_time[vid]
                    ap_trip_mode, ns_trip_mode = None, None
                    #
                    if pt_el_ap == IN and c_sl_ap == IN: ap_trip_mode = DIn_PIn
                    elif pt_el_ap == IN and c_sl_ap == OUT: ap_trip_mode = DIn_POut
                    elif pt_el_ap == OUT and c_sl_ap == IN: ap_trip_mode = DOut_PIn
                    elif pt_el_ap == OUT and c_sl_ap == OUT: ap_trip_mode = DOut_POut
                    else: assert False
                    #
                    if pt_el_ns == IN and c_sl_ns == IN: ns_trip_mode = DIn_PIn
                    elif pt_el_ns == IN and c_sl_ns == OUT: ns_trip_mode = DIn_POut
                    elif pt_el_ns == OUT and c_sl_ns == IN: ns_trip_mode = DOut_PIn
                    elif pt_el_ns == OUT and c_sl_ns == OUT: ns_trip_mode = DOut_POut
                    else: assert False
                    #
                    vehicle_prev_trip_position_time[vid] = (c_el_ter, c_el_ap, c_el_ns, et_ts)
                    #
                    with open(trip_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [vid, did,
                                   st_ts, et_ts, dur, fare,
                                   ap_trip_mode, ns_trip_mode, pt_time,
                                   year, month, day, hour,
                                   c_sl_ter, pt_el_ter]
                        writer.writerow(new_row)
                    #
                    # For filtered version
                    # Only consider trips whose start time is before 2 AM and after 6 AM
                    #
                    if AM2 <= hour and hour <= AM5:
                        continue
                    need2skip = False
                    for ys, ms, ds, hs in error_hours:
                        yyyy0 = 2000 + int(ys)
                        mm0, dd0, hh0 = map(int, [ms, ds, hs])
                        if (year == yyyy0) and (month == mm0) and (day == dd0) and (hour == hh0):
                            need2skip = True
                    if need2skip: continue
                    #
                    with open(trip_filtered_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [vid, did,
                                   st_ts, et_ts, dur, fare,
                                   ap_trip_mode, ns_trip_mode, pt_time,
                                   year, month, day, hour,
                                   c_sl_ter, pt_el_ter]
                        writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
