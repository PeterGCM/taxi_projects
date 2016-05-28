from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports._setting import DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS
from supports._setting import trips_dir, trip_prefix
from supports._setting import summary_dir, ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn
from supports.etc_functions import check_dir_create
from supports.logger import logging_msg
#
import datetime, time, csv
import pandas as pd
#
def run():
    check_dir_create(summary_dir)
    with open(ap_tm_num_dur_fare_fn, 'wt') as csvFile:
        writer = csv.writer(csvFile)
        header = ['yy', 'mm', 'dd', 'hh', 'day-of-week', 'ap-trip-mode', 'num-tm', 'total-dur', 'total-fare']
        writer.writerow(header)
    
    with open(ns_tm_num_dur_fare_fn, 'wt') as csvFile:
        writer = csv.writer(csvFile)
        header = ['yy', 'mm', 'dd', 'hh', 'day-of-week', 'ns-trip-mode', 'num-tm', 'total-dur', 'total-fare']
        writer.writerow(header)
    
    process_files('0908')
    
#     for y in xrange(9, 11):
#         for m in xrange(1, 13):
#             yymm = '%02d%02d' % (y, m) 
#             if yymm in ['0912', '1010']:
#                 continue
#             process_files(yymm)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
    #
    yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
    dd, hh = 1, 0
    cur_day_time = datetime.datetime(yyyy, mm, dd, hh)
    if mm == 12:
        next_yyyy, next_mm = yyyy + 1, 1
    else:
        next_yyyy, next_mm = yyyy, mm + 1
    last_day_time = datetime.datetime(next_yyyy, next_mm, dd, hh)
    #
    st_label = 'start-time'
    ap_tm_lable, ns_tm_lable = 'ap-trip-mode', 'ns-trip-mode' 
    dur_lable, fare_label = 'duration', 'fare'
    #
    ap_tm = [DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP]
    ns_tm = [DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS]
    #
    while cur_day_time != last_day_time:
        next_day_time = cur_day_time + datetime.timedelta(hours=1)
        st_timestamp, et_timestamp = time.mktime(cur_day_time.timetuple()), time.mktime(next_day_time.timetuple())
        #
        yyyy, mm, dd, hh = cur_day_time.year, cur_day_time.month, cur_day_time.day, cur_day_time.hour
        #    
        filtered_trip = trip_df[(st_timestamp <= trip_df[st_label]) & (trip_df[st_label] < et_timestamp)]
        #
        gp_f_trip = filtered_trip.groupby([ap_tm_lable])
        tm_num_totalDuration_totalFare = [[tm, 0, 0, 0] for tm in ap_tm]
        tm_num_df = gp_f_trip.count()[fare_label].to_frame('total_tm_num').reset_index()
        for tm, num in tm_num_df.values:
            tm_num_totalDuration_totalFare[tm][1] += num
        tm_dur_df = gp_f_trip.sum()[dur_lable].to_frame('total_tm_dur').reset_index()
        for tm, dur in tm_dur_df.values:
            tm_num_totalDuration_totalFare[tm][2] += dur
        tm_fare_df = gp_f_trip.sum()[fare_label].to_frame('total_tm_fare').reset_index()
        for tm, fare in tm_fare_df.values:
            tm_num_totalDuration_totalFare[tm][3] += fare
        save_as_csv(ap_tm_num_dur_fare_fn, yymm, dd, hh, tm_num_totalDuration_totalFare)
        #
        gp_f_trip = filtered_trip.groupby([ns_tm_lable])
        tm_num_totalDuration_totalFare = [[tm, 0, 0, 0] for tm in ns_tm]
        tm_num_df = gp_f_trip.count()[fare_label].to_frame('total_tm_num').reset_index()
        for tm, num in tm_num_df.values:
            tm_num_totalDuration_totalFare[tm][1] += num
        tm_dur_df = gp_f_trip.sum()[dur_lable].to_frame('total_tm_dur').reset_index()
        for tm, dur in tm_dur_df.values:
            tm_num_totalDuration_totalFare[tm][2] += dur
        tm_fare_df = gp_f_trip.sum()[fare_label].to_frame('total_tm_fare').reset_index()
        for tm, fare in tm_fare_df.values:
            tm_num_totalDuration_totalFare[tm][3] += fare
        save_as_csv(ns_tm_num_dur_fare_fn, yymm, dd, hh, tm_num_totalDuration_totalFare)
        #
        cur_day_time = next_day_time
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)

def save_as_csv(fn, yymm, dd, hh, _data):
    yy, mm = yymm[:2], yymm[2:]
    yyyy = 2000 + int(yy)
    cur_datetime = datetime.datetime(yyyy, int(mm), dd, hh)
    dow = cur_datetime.strftime("%a") 
    with open(fn, 'a') as csvFile:
        writer = csv.writer(csvFile)
        for tm, num, totalDur, totalFare in _data:
            writer.writerow([yy, mm, dd, hh, dow, tm, num, totalDur, totalFare])

if __name__ == '__main__':
    run()    
