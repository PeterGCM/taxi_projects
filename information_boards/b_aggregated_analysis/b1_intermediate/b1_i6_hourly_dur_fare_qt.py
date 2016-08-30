import __init__
#
from information_boards import SEC3600
from information_boards.a_overall_analysis import trips_dir, trip_prefix
from information_boards.b_aggregated_analysis import shift_pro_dur_dir, shift_pro_dur_prefix
from information_boards.b_aggregated_analysis import ap_trips_dir, ap_trip_prefix
from information_boards.b_aggregated_analysis import ns_trips_dir, ns_trip_prefix
from information_boards.b_aggregated_analysis import productivity_dir, productivity_prefix
from information_boards.b_aggregated_analysis.b1_intermediate import ALL_DUR, ALL_FARE, ALL_NUM
from information_boards.b_aggregated_analysis.b1_intermediate import AP_DUR, AP_FARE, AP_QUEUE, AP_NUM
from information_boards.b_aggregated_analysis.b1_intermediate import NS_DUR, NS_FARE, NS_QUEUE, NS_NUM
#
from taxi_common.file_handling_functions import remove_create_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, time, datetime


def run():
    remove_create_dir(productivity_dir)

    # init_multiprocessor()
    # count_num_jobs = 0
    # for yymm in ['1006', '1007', '1008', '1009', '1011', '1012']:
    #     put_task(process_files, [yymm])
    #     count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)

    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_files('1007')
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
    print 'handle the file; %s' % yymm
    begin_datetime = datetime.datetime(2009, 1, 1, 0)
    last_datetime = datetime.datetime(2011, 2, 1, 0)
    hourly_stats, time_period_order = {}, []
    while begin_datetime < last_datetime:
        yyyy, mm, dd, hh = begin_datetime.year, begin_datetime.month, begin_datetime.day, begin_datetime.hour
        k = (yyyy, mm, dd, hh)
        hourly_stats[k] = [0 for _ in range(len([ALL_DUR, ALL_FARE, ALL_NUM,
                                                 AP_DUR, AP_FARE, AP_QUEUE, AP_NUM,
                                                 NS_DUR, NS_FARE, NS_QUEUE, NS_NUM]))]
        time_period_order.append(k)
        begin_datetime += datetime.timedelta(hours=1)
    #
    st_label, et_label, dur_label, fare_label = 'start-time', 'end-time', 'duration', 'fare'
    qt_label = 'queueing-time'
    # Productive duration
    print yymm, 'Productive duration'
    yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
    with open('%s/%s%s.csv' % (shift_pro_dur_dir, shift_pro_dur_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            dd, hh = eval(row[hid['dd']]), eval(row[hid['hh']])
            hourly_stats[(yyyy, mm, dd, hh)][ALL_DUR] += eval(row[hid['pro-dur']]) * 60  # unit change; Minute -> Second
    # Total fare
    print yymm, 'Total fare'
    with open('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            st_ts, et_ts = eval(row[hid[st_label]]), eval(row[hid[et_label]])
            dur, fare = eval(row[hid[dur_label]]), eval(row[hid[fare_label]])
            sum_prop_fare_dur(hourly_stats, st_ts, et_ts, dur, fare, ALL_FARE, ALL_NUM, None)

    # Sum up fare, duration and queue time
    print yymm, 'Sum up fare, duration and queue time'
    for dir_path, file_prefix, id_DUR, id_FARE, id_QUEUE, id_NUM in [(ap_trips_dir, ap_trip_prefix,
                                                                      AP_DUR, AP_FARE, AP_QUEUE, AP_NUM),
                                                                     (ns_trips_dir, ns_trip_prefix,
                                                                      NS_DUR, NS_FARE, NS_QUEUE, NS_NUM)]:
        with open('%s/%s%s.csv' % (dir_path, file_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                st_ts, et_ts = eval(row[hid[st_label]]), eval(row[hid[et_label]])
                dur, fare = eval(row[hid[dur_label]]), eval(row[hid[fare_label]])
                qt = eval(row[hid[qt_label]])
                #
                sum_prop_fare_dur(hourly_stats, st_ts, et_ts, dur, fare, id_FARE, id_NUM, id_DUR)
                sum_queueing_time(hourly_stats, st_ts, qt, id_QUEUE)
    # Generate .csv file
    print yymm, 'Generate .csv file'
    with open('%s/%s%s.csv' % (productivity_dir, productivity_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'hh',
                  'all-duration', 'all-fare', 'all-num',
                  'ap-duration', 'ap-fare', 'ap-queueing-time', 'ap-num',
                  'ns-duration', 'ns-fare', 'ns-queueing-time', 'ns-num']
        writer.writerow(header)
        for yyyy, mm, dd, hh in time_period_order:
            all_dur, all_fare, all_num, \
            ap_dur, ap_fare, ap_qt, ap_num, \
            ns_dur, ns_fare, ns_qt, ns_num = hourly_stats[(yyyy, mm, dd, hh)]
            #
            writer.writerow([yyyy - 2000, mm, dd, hh,
                             all_dur, all_fare, all_num,
                             ap_dur, ap_fare, ap_qt, ap_num,
                             ns_dur, ns_fare, ns_qt, ns_num
                             ])
    print 'end the file; %s' % yymm


def sum_prop_fare_dur(hourly_stats, st_ts, et_ts, dur, fare, id_FARE, id_NUM, id_DUR=None):
    def add_prop_fare_dur(dur_within_slot, dur, fare, id_FARE, id_DUR):
        prop = dur_within_slot / float(dur)
        hourly_stats[(et_dt.year, et_dt.month,
                      et_dt.day, et_dt.hour)][id_FARE] += fare * prop
        if id_DUR is not None:
            hourly_stats[(st_dt.year, st_dt.month,
                          st_dt.day, st_dt.hour)][id_DUR] += dur_within_slot
    #
    st_dt, et_dt = datetime.datetime.fromtimestamp(st_ts), datetime.datetime.fromtimestamp(et_ts)
    hourly_stats[(st_dt.year, st_dt.month,
                  st_dt.day, st_dt.hour)][id_NUM] += 1
    #
    if st_dt.hour == et_dt.hour:
        hourly_stats[(st_dt.year, st_dt.month,
                      st_dt.day, st_dt.hour)][id_FARE] += fare
        if id_DUR is not None:
            hourly_stats[(st_dt.year, st_dt.month,
                          st_dt.day, st_dt.hour)][id_DUR] += dur
    else:
        next_ts_dt = datetime.datetime(st_dt.year, st_dt.month, st_dt.day, st_dt.hour) + datetime.timedelta(hours=1)
        tg_year, tg_month, tg_day, tg_hour = \
            next_ts_dt.year, next_ts_dt.month, next_ts_dt.day, next_ts_dt.hour
        tg_dt = datetime.datetime(tg_year, tg_month, tg_day, tg_hour)
        tg_ts = time.mktime(tg_dt.timetuple())
        dur_within_slot = tg_ts - st_ts
        add_prop_fare_dur(dur_within_slot, dur, fare, id_FARE, id_DUR)
        while True:
            if tg_dt.hour == et_dt.hour:
                dur_within_slot = et_ts - tg_ts
                add_prop_fare_dur(dur_within_slot, dur, fare, id_FARE, id_DUR)
                break
            dur_within_slot = SEC3600
            add_prop_fare_dur(dur_within_slot, dur, fare, id_FARE, id_DUR)
            #
            tg_dt += datetime.timedelta(hours=1)


def sum_queueing_time(hourly_total, st_ts, qt, id_QUEUE):
    st_dt = datetime.datetime.fromtimestamp(st_ts)
    q_jt_ts = st_ts - qt
    q_jt_dt = datetime.datetime.fromtimestamp(q_jt_ts)
    if q_jt_dt.hour == st_dt.hour:
        hourly_total[(st_dt.year, st_dt.month,
                      st_dt.day, st_dt.hour)][id_QUEUE] += qt
    else:
        next_ts_dt = datetime.datetime(q_jt_dt.year, q_jt_dt.month,
                                       q_jt_dt.day, q_jt_dt.hour) + datetime.timedelta(hours=1)
        tg_year, tg_month, tg_day, tg_hour = \
            next_ts_dt.year, next_ts_dt.month, next_ts_dt.day, next_ts_dt.hour
        tg_dt = datetime.datetime(tg_year, tg_month, tg_day, tg_hour)
        tg_ts = time.mktime(tg_dt.timetuple())
        hourly_total[(q_jt_dt.year, q_jt_dt.month,
                      q_jt_dt.day, q_jt_dt.hour)][id_QUEUE] += tg_ts - q_jt_ts
        while True:
            if tg_dt.hour == st_dt.hour:
                hourly_total[(st_dt.year, st_dt.month,
                              st_dt.day, st_dt.hour)][id_QUEUE] += st_ts - tg_ts
                break
            hourly_total[(tg_dt.year, tg_dt.month,
                          tg_dt.day, tg_dt.hour)][id_QUEUE] += SEC3600
            tg_dt += datetime.timedelta(hours=1)


if __name__ == '__main__':
    run()