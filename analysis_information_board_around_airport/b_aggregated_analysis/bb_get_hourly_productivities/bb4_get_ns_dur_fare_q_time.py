from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
from supports.etc_functions import remove_creat_dir
from supports._setting import Q_LIMIT_MIN, SEC3600
from supports._setting import TIME_ALARM
from supports._setting import ns_trip_prefix
from supports._setting import nightsafari_trips_dir
from supports._setting import ns_dur_fare_q_time_dir, ns_dur_fare_q_time_prefix
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime, time
#
NS_DUR, NS_FARE, NS_QUEUE = range(3)
#
def run():
    remove_creat_dir(ns_dur_fare_q_time_dir)
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
#             process_files('1007')
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_files(yymm):
    old_time = time.time()
    print 'handle the file; %s' % yymm
    begin_datetime = datetime.datetime(2009, 1, 1, 0) 
    last_datetime = datetime.datetime(2011, 2, 1, 0)
    hourly_total, time_period_order = {}, []
    while begin_datetime < last_datetime:
        yyyy, mm, dd, hh = begin_datetime.year, begin_datetime.month, begin_datetime.day, begin_datetime.hour
        k = (yyyy, mm, dd, hh)
        hourly_total[k] = [0 for _ in range(len([NS_DUR, NS_FARE, NS_QUEUE]))]
        time_period_order.append(k)
        begin_datetime += datetime.timedelta(hours=1)
    #
    st_label, et_label, dur_label, fare_label = 'start-time', 'end-time', 'duration', 'fare'
    ns_qt_label = 'ns-queue-time'
    # Night Safari fare, duration and queue time
    with open('%s/%s%s.csv' % (nightsafari_trips_dir, ns_trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        for row in reader:
            st_ts, et_ts = eval(row[hid[st_label]]), eval(row[hid[et_label]])
            dur, fare = eval(row[hid[dur_label]]), eval(row[hid[fare_label]])
            ns_qt = eval(row[hid[ns_qt_label]])
            #
            st_dt, et_dt = datetime.datetime.fromtimestamp(st_ts), datetime.datetime.fromtimestamp(et_ts)
            # Duration and queue time
            if st_dt.hour == et_dt.hour: 
                hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][NS_DUR] += dur
                hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][NS_FARE] += fare
            else:
                next_ts_dt = datetime.datetime(st_dt.year, st_dt.month, st_dt.day, st_dt.hour) + datetime.timedelta(hours=1)
                tg_year, tg_month, tg_day, tg_hour = \
                        next_ts_dt.year, next_ts_dt.month, next_ts_dt.day, next_ts_dt.hour
                tg_dt = datetime.datetime(tg_year, tg_month, tg_day, tg_hour)
                tg_ts = time.mktime(tg_dt.timetuple())
                dur_within_slot = tg_ts - st_ts
                prop = dur_within_slot / dur
                hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][NS_DUR] += dur_within_slot
                hourly_total[(et_dt.year, et_dt.month,
                              et_dt.day, et_dt.hour)][NS_FARE] += fare * prop
                while True:
                    if tg_dt.hour == et_dt.hour:
                        dur_within_slot = et_ts - tg_ts 
                        prop = dur_within_slot / dur
                        hourly_total[(et_dt.year, et_dt.month,
                              et_dt.day, et_dt.hour)][NS_DUR] += dur_within_slot
                        hourly_total[(et_dt.year, et_dt.month,
                              et_dt.day, et_dt.hour)][NS_FARE] += fare * prop      
                        break
                    prop = SEC3600 / dur
                    hourly_total[(tg_dt.year, tg_dt.month,
                              tg_dt.day, tg_dt.hour)][NS_DUR] += SEC3600
                    hourly_total[(tg_dt.year, tg_dt.month,
                              tg_dt.day, tg_dt.hour)][NS_DUR] += fare * prop
                    tg_dt += datetime.timedelta(hours=1)
            # Queue time
            if ns_qt < Q_LIMIT_MIN:
                ns_qt = Q_LIMIT_MIN
            q_jt_ts = st_ts - ns_qt
            q_jt_dt = datetime.datetime.fromtimestamp(q_jt_ts)
            if q_jt_dt.hour == st_dt.hour: 
                hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][NS_QUEUE] += ns_qt
            else:
                next_ts_dt = datetime.datetime(q_jt_dt.year, q_jt_dt.month,
                                               q_jt_dt.day, q_jt_dt.hour) + datetime.timedelta(hours=1)
                tg_year, tg_month, tg_day, tg_hour = \
                        next_ts_dt.year, next_ts_dt.month, next_ts_dt.day, next_ts_dt.hour
                tg_dt = datetime.datetime(tg_year, tg_month, tg_day, tg_hour)
                tg_ts = time.mktime(tg_dt.timetuple())
                hourly_total[(q_jt_dt.year, q_jt_dt.month,
                              q_jt_dt.day, q_jt_dt.hour)][NS_QUEUE] += tg_ts - q_jt_ts
                while True:
                    if tg_dt.hour == st_dt.hour:
                        hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][NS_QUEUE] += st_ts - tg_ts
                        break
                    hourly_total[(tg_dt.year, tg_dt.month,
                              tg_dt.day, tg_dt.hour)][NS_QUEUE] += SEC3600
                    tg_dt += datetime.timedelta(hours=1)
            if (time.time() - old_time) > TIME_ALARM == 0:
                old_time = time.time()
                print 'handling; %s' % yymm
    with open('%s/%s%s.csv' % (ns_dur_fare_q_time_dir, ns_dur_fare_q_time_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'hh', 'ns-duration', 'ns-fare', 'ns-queue-time']
        writer.writerow(header)
        for yyyy, mm, dd, hh in time_period_order:
            ns_dur, ns_fare, ns_qt = hourly_total[(yyyy, mm, dd, hh)] 
            writer.writerow([yyyy - 2000, mm, dd, hh, ns_dur, ns_fare, ns_qt])
    print 'end the file; %s' % yymm

if __name__ == '__main__':
    run()
