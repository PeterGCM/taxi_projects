import __init__
#
from information_boards.b_aggregated_analysis import ap_trips_dir, ap_trip_prefix
from information_boards.b_aggregated_analysis import ns_trips_dir, ns_trip_prefix
from information_boards.b_aggregated_analysis import ap_ep_dir, ap_ep_prefix
from information_boards.b_aggregated_analysis import ns_ep_dir, ns_ep_prefix
from information_boards.b_aggregated_analysis import hourly_stats_fpath
#
from taxi_common.file_handling_functions import remove_create_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime


def run():
    remove_create_dir(ap_ep_dir); remove_create_dir(ns_ep_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_files(yymm)
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
    yy, mm = yymm[:2], yymm[-2:]
    print 'handle the file; %s' % yymm
    #
    ap_gen_productivity, ns_gen_productivity = {}, {}
    with open(hourly_stats_fpath) as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            yyyy, mm, dd, hh = 2000 + eval(row[hid['yy']]), eval(row[hid['mm']]), eval(row[hid['dd']]), eval(
                row[hid['hh']])
            ap_gen_productivity[(yyyy, mm, dd, hh)] = eval(row[hid['ap-gen-productivity']])
            ns_gen_productivity[(yyyy, mm, dd, hh)] = eval(row[hid['ns-gen-productivity']])
    #
    for dir_path, file_prefix, ep_dir, ep_prefix, gen_productivity in [(ap_trips_dir, ap_trip_prefix, ap_ep_dir, ap_ep_prefix, ap_gen_productivity),
                                                                       (ns_trips_dir, ns_trip_prefix, ns_ep_dir, ns_ep_prefix, ns_gen_productivity)]:
        with open('%s/%s%s.csv' % (dir_path, file_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (ep_dir, ep_prefix, yymm), 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile) 
                new_headers = ['start-time', 'did', 'duration', 'fare',
                               'trip-mode', 'queueing-time', 'economic-profit',
                               'yy', 'mm', 'dd', 'hh']
                writer.writerow(new_headers)
                #
                for row in reader:
                    st_ts = eval(row[hid['start-time']])
                    st_dt = datetime.datetime.fromtimestamp(st_ts)
                    k = (st_dt.year, st_dt.month, st_dt.day, st_dt.hour)
                    qt = eval(row[hid['queueing-time']])
                    dur, fare = eval(row[hid['duration']]), eval(row[hid['fare']]) 
                    eco_profit = fare - gen_productivity[k] * (qt + dur)
                    #
                    writer.writerow([st_ts, row[hid['did']], dur, fare,
                                     row[hid['trip-mode']], qt, eco_profit,
                                     yy, mm, st_dt.day, st_dt.hour])
    #
    print 'end the file; %s' % yymm
    
if __name__ == '__main__':
    run()
