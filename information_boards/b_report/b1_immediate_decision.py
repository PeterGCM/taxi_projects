import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import trip_ap_summary_fpath, trip_ns_summary_fpath
from information_boards import NUM, DUR, FARE
from information_boards import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
#
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import csv
import time, datetime

logger = get_logger()


def run():
    def summary(yymm):
        logger.info('handle the file; %s' % yymm)
        yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
        dd, hh = 1, 0
        cur_day_time = datetime.datetime(yyyy, mm, dd, hh)
        if mm == 12:
            next_yyyy, next_mm = yyyy + 1, 1
        else:
            next_yyyy, next_mm = yyyy, mm + 1
        last_day_time = datetime.datetime(next_yyyy, next_mm, dd, hh)
        #
        trip_df = pd.read_csv('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm))
        while cur_day_time != last_day_time:
            next_day_time = cur_day_time + datetime.timedelta(hours=1)
            st_timestamp, et_timestamp = time.mktime(cur_day_time.timetuple()), time.mktime(next_day_time.timetuple())
            #
            yyyy, mm, dd, hh = cur_day_time.year, cur_day_time.month, cur_day_time.day, cur_day_time.hour
            #
            filtered_trip = trip_df[(st_timestamp <= trip_df['startTime']) & (trip_df['startTime'] < et_timestamp)]
            if len(filtered_trip) != 0:
                for fn, label in [(trip_ap_summary_fpath, 'tripModeAP'),
                                  (trip_ns_summary_fpath, 'tripModeNS')]:
                    gp_f_trip = filtered_trip.groupby([label])
                    num_totalDuration_totalFare_tm = [[0, 0, 0, tm] for tm in [DIn_PIn, DIn_POut, DOut_PIn, DOut_POut]]
                    tm_num_df = gp_f_trip.count()['fare'].to_frame('totalTmNum').reset_index()
                    for tm, num in tm_num_df.values:
                        num_totalDuration_totalFare_tm[int(tm)][NUM] += num
                    #
                    tm_dur_df = gp_f_trip.sum()['duration'].to_frame('totalTmDur').reset_index()
                    for tm, dur in tm_dur_df.values:
                        num_totalDuration_totalFare_tm[int(tm)][DUR] += dur
                    #
                    tm_fare_df = gp_f_trip.sum()['fare'].to_frame('totalTmFare').reset_index()
                    for tm, fare in tm_fare_df.values:
                        num_totalDuration_totalFare_tm[int(tm)][FARE] += fare
                    dow = cur_day_time.strftime("%a")
                    with open(fn, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        for num, totalDur, totalFare, tm in num_totalDuration_totalFare_tm:
                            writer.writerow([yyyy, mm, dd, hh, dow, num, totalDur, totalFare, tm])
            cur_day_time = next_day_time
        logger.info('end the file; %s' % yymm)
    #
    logger.info('Start')
    for fn in [trip_ap_summary_fpath, trip_ns_summary_fpath]:
        with open(fn, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['year', 'month', 'day', 'hour', 'dayOfWeek', 'totalNum', 'totalDur', 'totalFare', 'tripMode']
            writer.writerow(header)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            summary(yymm)


if __name__ == '__main__':
    run()
