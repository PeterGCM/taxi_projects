from __future__ import division
import os, sys
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import trips_dir, hourly_summary
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports.etc_functions import get_all_files, remove_creat_dir
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports.logger import logging_msg
#
import pandas as pd
import datetime, time, csv
#
def run():
    remove_creat_dir(hourly_summary)
    csv_files = get_all_files(trips_dir, 'whole-trip-', '.csv')
    #
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
        put_task(process_file, [fn])
#         process_file(fn)
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
        
def process_file(fn):
    _, _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm 
    logging_msg('handle the file; %s' % yymm)
    new_fn = '%s/hourly-summary-%s.csv' % (hourly_summary, yymm)
    with open(new_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        headers = ['yy', 'mm', 'dow', 'hh', 'trip-mode', 'total-num', 'total-fare']
        writer.writerow(headers)
    #
    trip_df = pd.read_csv('%s/%s' % (trips_dir, fn))
    
    yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
    dd, hh = 1, 0
    cur_datetime = datetime.datetime(yyyy, mm, dd, hh)
    if mm == 12:
        next_yyyy, next_mm = yyyy + 1, 1
    else:
        next_yyyy, next_mm = yyyy, mm + 1
    last_day_time = datetime.datetime(next_yyyy, next_mm, dd, hh)
    #
    st_label = 'start-time'
    fare_label = 'fare'
    tms = [DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP]
    while cur_datetime != last_day_time:
        next_datetime = cur_datetime + datetime.timedelta(hours=1)
        cur_timestamp, next_timestamp = time.mktime(cur_datetime.timetuple()), time.mktime(next_datetime.timetuple())
        filtered_trip = trip_df[(cur_timestamp <= trip_df[st_label]) & (trip_df[st_label] < next_timestamp)]
        #
        tm_grouped = filtered_trip.groupby(['trip-mode'], sort=True)
        yy, mm = yymm[:2], yymm[2:]
        dow, hh = cur_datetime.strftime("%a"), cur_datetime.hour 
        with open(new_fn, 'a') as csvFile:
            writer = csv.writer(csvFile)
            tm_totalNum_totalFare = zip(tms, list(tm_grouped.count()[fare_label]), list(tm_grouped.sum()[fare_label]))
            for tm, totalNum, totalFare in tm_totalNum_totalFare:
                writer.writerow([yy, mm, dow, hh, tm, totalNum, totalFare])
        cur_datetime = next_datetime
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
    
if __name__ == '__main__':
    run()