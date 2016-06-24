import __init__  # @UnresolvedImport # @UnusedImport
#
from init_project import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from a_overall_analysis.__init__ import trips_dir, trip_prefix  # @UnresolvedImport
from a_overall_analysis.__init__ import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn  # @UnresolvedImport
from __init__ import NUM, DUR, FARE
#
import datetime, time, csv
import pandas as pd
#
def run():
    init_csv_files()
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)

def init_csv_files():
    for fn in [ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn]:
        with open(fn, 'wt') as csvFile:
            writer = csv.writer(csvFile)
            header = ['yy', 'mm', 'dd', 'hh', 'day-of-week', 'total-num', 'total-dur', 'total-fare', 'trip-mode']
            writer.writerow(header)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
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
    while cur_day_time != last_day_time:
        next_day_time = cur_day_time + datetime.timedelta(hours=1)
        st_timestamp, et_timestamp = time.mktime(cur_day_time.timetuple()), time.mktime(next_day_time.timetuple())
        #
        yyyy, mm, dd, hh = cur_day_time.year, cur_day_time.month, cur_day_time.day, cur_day_time.hour
        #    
        filtered_trip = trip_df[(st_timestamp <= trip_df[st_label]) & (trip_df[st_label] < et_timestamp)]
        for fn, label in [(ap_tm_num_dur_fare_fn, ap_tm_lable), (ns_tm_num_dur_fare_fn, ns_tm_lable)]:
            gp_f_trip = filtered_trip.groupby([label])
            num_totalDuration_totalFare_tm = [[0, 0, 0, tm] for tm in [DIn_PIn, DIn_POut, DOut_PIn, DOut_POut]]
            tm_num_df = gp_f_trip.count()[fare_label].to_frame('total_tm_num').reset_index()
            for tm, num in tm_num_df.values:
                num_totalDuration_totalFare_tm[tm][NUM] += num
            #
            tm_dur_df = gp_f_trip.sum()[dur_lable].to_frame('total_tm_dur').reset_index()
            for tm, dur in tm_dur_df.values:
                num_totalDuration_totalFare_tm[tm][DUR] += dur
            #
            tm_fare_df = gp_f_trip.sum()[fare_label].to_frame('total_tm_fare').reset_index()
            for tm, fare in tm_fare_df.values:
                num_totalDuration_totalFare_tm[tm][FARE] += fare
            save_as_csv(fn, yymm, dd, hh, num_totalDuration_totalFare_tm)
        cur_day_time = next_day_time
    print 'handle the file; %s' % yymm

def save_as_csv(fn, yymm, dd, hh, _data):
    yy, mm = yymm[:2], yymm[2:]
    yyyy = 2000 + int(yy)
    cur_datetime = datetime.datetime(yyyy, int(mm), dd, hh)
    dow = cur_datetime.strftime("%a") 
    with open(fn, 'a') as csvFile:
        writer = csv.writer(csvFile)
        for num, totalDur, totalFare, tm in _data:
            writer.writerow([yy, mm, dd, hh, dow, num, totalDur, totalFare, tm])

if __name__ == '__main__':
    run()    
