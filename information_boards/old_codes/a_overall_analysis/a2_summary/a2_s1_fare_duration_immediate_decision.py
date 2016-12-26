#
import csv
import datetime
import time

import pandas as pd

from information_boards import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from information_boards.old_codes.a_overall_analysis import NUM, DUR, FARE
from information_boards.old_codes.a_overall_analysis import ap_tm_num_dur_fare_fpath, ns_tm_num_dur_fare_fpath
from information_boards.old_codes.a_overall_analysis import trips_dpath, trip_prefix


def run():
    for fn in [ap_tm_num_dur_fare_fpath, ns_tm_num_dur_fare_fpath]:
        with open(fn, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['yy', 'mm', 'dd', 'hh', 'day-of-week', 'total-num', 'total-dur', 'total-fare', 'trip-mode']
            writer.writerow(header)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)


def process_files(yymm):
    print 'handle the file; %s' % yymm
    yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
    dd, hh = 1, 0
    cur_day_time = datetime.datetime(yyyy, mm, dd, hh)
    if mm == 12:
        next_yyyy, next_mm = yyyy + 1, 1
    else:
        next_yyyy, next_mm = yyyy, mm + 1
    last_day_time = datetime.datetime(next_yyyy, next_mm, dd, hh)
    #
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dpath, trip_prefix, yymm))
    while cur_day_time != last_day_time:
        next_day_time = cur_day_time + datetime.timedelta(hours=1)
        st_timestamp, et_timestamp = time.mktime(cur_day_time.timetuple()), time.mktime(next_day_time.timetuple())
        #
        yyyy, mm, dd, hh = cur_day_time.year, cur_day_time.month, cur_day_time.day, cur_day_time.hour
        #    
        filtered_trip = trip_df[(st_timestamp <= trip_df['start-time']) & (trip_df['start-time'] < et_timestamp)]
        if len(filtered_trip) != 0:
            for fn, label in [(ap_tm_num_dur_fare_fpath, 'ap-trip-mode'), (ns_tm_num_dur_fare_fpath, 'ns-trip-mode')]:
                gp_f_trip = filtered_trip.groupby([label])
                num_totalDuration_totalFare_tm = [[0, 0, 0, tm] for tm in [DIn_PIn, DIn_POut, DOut_PIn, DOut_POut]]
                tm_num_df = gp_f_trip.count()['fare'].to_frame('total_tm_num').reset_index()
                for tm, num in tm_num_df.values:
                    num_totalDuration_totalFare_tm[int(tm)][NUM] += num
                #
                tm_dur_df = gp_f_trip.sum()['duration'].to_frame('total_tm_dur').reset_index()
                for tm, dur in tm_dur_df.values:
                    num_totalDuration_totalFare_tm[int(tm)][DUR] += dur
                #
                tm_fare_df = gp_f_trip.sum()['fare'].to_frame('total_tm_fare').reset_index()
                for tm, fare in tm_fare_df.values:
                    num_totalDuration_totalFare_tm[int(tm)][FARE] += fare
                dow = cur_day_time.strftime("%a")
                with open(fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    for num, totalDur, totalFare, tm in num_totalDuration_totalFare_tm:
                        writer.writerow([yyyy - 2000, mm, dd, hh, dow, num, totalDur, totalFare, tm])
        cur_day_time = next_day_time
    print 'end the file; %s' % yymm


if __name__ == '__main__':
    run()    
