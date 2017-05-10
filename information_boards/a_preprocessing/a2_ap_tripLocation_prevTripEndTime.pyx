import __init__
#
'''

'''
#
from information_boards import taxi_home
from information_boards import dpaths, prefixs
from information_boards import AM2, AM5
from information_boards import error_hours
#
from taxi_common.geo_functions import get_ap_polygons
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.log_handling_functions import get_logger
#
from datetime import datetime
import csv

logger = get_logger()

of_dpath = dpaths['trip', 'ap']
of_prefixs = prefixs['trip', 'ap']

try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        yy, mm = yymm[:2], yymm[-2:]
        yyyy = str(2000 + int(yy))
        normal_file = taxi_home + '/%s/%s/trips/trips-%s-normal.csv' % (yyyy, mm, yymm)
        ext_file = taxi_home + '/%s/%s/trips/trips-%s-normal-ext.csv' % (yyyy, mm, yymm)
        #
        year, month = map(int, [yyyy, mm])
        ap_polygons = get_ap_polygons()
        handling_day, vid_lastLocTime = 0, {}
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
                    did = int(row2[hid2['driver-id']])
                    if did == -1:
                        continue
                    ts_st, ts_et = map(eval, [row1[hid1[l]] for l in ['start-time', 'end-time']])
                    day, hour = map(int, [row1[hid1[l]] for l in ['start-time', 'end-time']])
                    #
                    need2skip = False
                    for ys, ms, ds, hs in error_hours:
                        yyyy0 = 2000 + int(ys)
                        mm0, dd0, hh0 = map(int, [ms, ds, hs])
                        if (year == yyyy0) and (month == mm0) and (day == dd0) and (hour == hh0):
                            need2skip = True
                            break
                    if need2skip: continue
                    dt_st = datetime.fromtimestamp(ts_st)
                    if dt_st.day == 1 and dt_st.hour <= AM5:
                        continue
                    if AM2 <= dt_st.hour and dt_st.hour <= AM5:
                        continue
                    if dt_st.day != handling_day and dt_st.hour == AM5 + 1:
                        handling_day, vid_lastLocTime = dt_st.day, {}
                        ofpath = '%s/ap-%s%s%02d.csv' % (of_dpath, of_prefixs, yymm, handling_day)
                        with open(ofpath, 'wt') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            new_headers = ['vid', 'did',
                                           'startTime', 'endTime', 'duration', 'fare',
                                           'pickUpTerminal',
                                           'prevEndTerminal', 'prevTripEndTime',
                                           'year', 'month', 'day', 'hour']
                            writer.writerow(new_headers)
                    vid = int(row1[hid1['vehicle-id']])
                    dur, fare = [row1[hid1[l]] for l in ['duration', 'fare']]
                    s_long, s_lat, e_long, e_lat = (eval(row1[hid1[l]])
                                                    for l in ['start-long', 'start-lat', 'end-long', 'end-lat'])
                    cur_start_ter, cur_end_ter = 'X', 'X'
                    for ap_polygon in ap_polygons:
                        if cur_start_ter == 'X':
                            if ap_polygon.is_including((s_long, s_lat)):
                                cur_start_ter = ap_polygon.name
                        if cur_end_ter == 'X':
                            if ap_polygon.is_including((e_long, e_lat)):
                                cur_end_ter = ap_polygon.name
                        if cur_start_ter != 'X' and cur_end_ter != 'X':
                            break
                    if not vid_lastLocTime.has_key(vid):
                        vid_lastLocTime[vid] = (cur_end_ter, ts_et)
                        continue
                    prevEndTerminal, prevTripEndTime = vid_lastLocTime[vid]
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [vid, did,
                                   ts_st, ts_et, dur, fare,
                                   cur_start_ter,
                                   prevEndTerminal, prevTripEndTime,
                                   year, month, day, hour]
                        writer.writerow(new_row)
                    vid_lastLocTime[vid] = (cur_end_ter, ts_et)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run(yymm)
