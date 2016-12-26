import __init__
#
'''

'''
#
from information_boards import shift_dpath, shift_prefix
from information_boards import trip_dpath, trip_prefix
from information_boards import queueingTime_ap_dpath, queueingTime_ap_prefix
from information_boards import queueingTime_ns_dpath, queueingTime_ns_prefix
from information_boards import productivity_dpath, productivity_prefix
from information_boards import shiftProDur_dpath, shiftProDur_prefix
from information_boards import AM2, AM5
from information_boards import SEC3600, SEC60
from information_boards import ALL_DUR, ALL_FARE, ALL_NUM
from information_boards import AP_DUR, AP_FARE, AP_QUEUE, AP_NUM
from information_boards import NS_DUR, NS_FARE, NS_QUEUE, NS_NUM
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv, gzip
import time, datetime

logger = get_logger()


def run():
    for dpath in [productivity_dpath, shiftProDur_dpath]:
        check_dir_create(dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_file(yymm)
            # put_task(productive_duration, [yymm])
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        productivity_fpath = '%s/%s%s.csv' % (productivity_dpath, productivity_prefix, yymm)
        if check_path_exist(productivity_fpath):
            logger.info('Already handled; %s' % yymm)
            return
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
        st_label, et_label, dur_label, fare_label = 'startTime', 'endTime', 'duration', 'fare'
        qt_label = 'queueingTime'
        #
        logger.info('Productive duration; %s' % yymm)
        yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
        with open('%s/%s%s.csv' % (shiftProDur_dpath, shiftProDur_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                dd, hh = eval(row[hid['dd']]), eval(row[hid['hh']])
                hourly_stats[(yyyy, mm, dd, hh)][ALL_DUR] += eval(row[hid['pro-dur']]) * SEC60  # unit change; Minute -> Second
        #
        logger.info('Total fare; %s' % yymm)
        with open('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                st_ts, et_ts = eval(row[hid[st_label]]), eval(row[hid[et_label]])
                dur, fare = eval(row[hid[dur_label]]), eval(row[hid[fare_label]])
                sum_prop_fare_dur(hourly_stats, st_ts, et_ts, dur, fare, ALL_FARE, ALL_NUM, None)

        #
        logger.info('Sum up fare, duration and queue time; %s' % yymm)
        for dir_path, file_prefix, id_DUR, id_FARE, id_QUEUE, id_NUM in [(queueingTime_ap_dpath, queueingTime_ap_prefix,
                                                                          AP_DUR, AP_FARE, AP_QUEUE, AP_NUM),
                                                                         (queueingTime_ns_dpath, queueingTime_ns_prefix,
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
        #
        logger.info('Generate .csv file; %s' % yymm)
        with open(productivity_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['yy', 'mm', 'dd', 'hh',
                      'allDuration', 'allFare', 'allNum',
                      'apDuration', 'apFare', 'apQueueingTime', 'apNum',
                      'nsDuration', 'nsFare', 'nsQueueingTime', 'nsNum']
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
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


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


def productive_duration(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        productive_state = ['dur%d' % x for x in [0, 3, 4, 5, 6, 7, 8, 9, 10]]
        with gzip.open('%s/%s%s.csv.gz' % (shift_dpath, shift_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (shiftProDur_dpath, shiftProDur_prefix, yymm), 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_headers = ['yy', 'mm', 'dd', 'hh', 'vid', 'did', 'pro-dur']
                writer.writerow(new_headers)
                for row in reader:
                    vid, did = row[hid['vehicle-id']], row[hid['driver-id']]
                    #
                    # Only consider trips whose start time is before 2 AM and after 6 AM
                    #
                    hh = eval(row[hid['hour']])
                    if AM2 <= hh and hh <= AM5:
                        continue
                    #
                    productive_duration = sum(int(row[hid[dur]]) for dur in productive_state)
                    writer.writerow([row[hid['year']][-2:], row[hid['month']], row[hid['day']], row[hid['hour']],
                                     vid, did, productive_duration])
        logger.info('end the file; %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
