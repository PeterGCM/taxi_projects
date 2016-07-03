import __init__  # @UnresolvedImport # @UnusedImport
#
from b_aggregated_analysis.__init__ import hourly_productivity_fn, zero_duration_timeslots
from b_aggregated_analysis.__init__ import ap_trips_dir, ap_trip_prefix
from b_aggregated_analysis.__init__ import ns_trips_dir, ns_trip_prefix
from b_aggregated_analysis.__init__ import ap_ep_dir, ap_ep_prefix
from b_aggregated_analysis.__init__ import ns_ep_dir, ns_ep_prefix
from b_aggregated_analysis.b2_summary.__init__ import GENERAL
#
from taxi_common.file_handling_functions import check_file_exist, get_all_files, load_pickle_file, remove_creat_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
if not check_file_exist(hourly_productivity_fn):
    from b_aggregated_analysis.b2_summary import run as summary_run
    summary_run()
#
omitted_timeslots = []
for l, ts in load_pickle_file(zero_duration_timeslots):
    if l == GENERAL:
        yyyy, mm, dd, hh = 2000 + eval(ts[0]), eval(ts[1]), eval(ts[2]), eval(ts[3])
        omitted_timeslots.append((yyyy, mm, dd, hh))
#
ap_out_productivity, ns_out_productivity = {}, {}
with open(hourly_productivity_fn) as r_csvfile:
    reader = csv.reader(r_csvfile)
    headers = reader.next()
    hid = {h : i for i, h in enumerate(headers)}
    for row in reader:
        yyyy, mm, dd, hh = 2000 + eval(row[hid['yy']]), eval(row[hid['mm']]), eval(row[hid['dd']]), eval(row[hid['hh']])
        if (yyyy, mm, dd, hh) in omitted_timeslots:
            continue  
        ap_out_productivity[(yyyy, mm, dd, hh)] = eval(row[hid['ap-out-productivity']])
        ns_out_productivity[(yyyy, mm, dd, hh)] = eval(row[hid['ns-out-productivity']])


def run():
    remove_creat_dir(ap_ep_dir); remove_creat_dir(ns_ep_dir)
    #
    # init_multiprocessor()
    # count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)
            # put_task(process_files, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def process_files(yymm):
    yy, mm = yymm[:2], yymm[-2:]
    print 'handle the file; %s' % yymm 
    for dir_path, file_prefix, ep_dir, ep_prefix, out_productivity in [(ap_trips_dir, ap_trip_prefix, ap_ep_dir, ap_ep_prefix, ap_out_productivity), 
                                                     (ns_trips_dir, ns_trip_prefix, ns_ep_dir, ns_ep_prefix, ns_out_productivity)]:
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
                    if k in omitted_timeslots:
                        continue
                    qt = eval(row[hid['queue-time']])
                    dur, fare = eval(row[hid['duration']]), eval(row[hid['fare']]) 
                    eco_profit = fare - out_productivity[k] * (qt + dur)
                    #
                    writer.writerow([st_ts, row[hid['did']], dur, fare,
                                     row[hid['trip-mode']], qt, eco_profit,
                                     yy, mm, st_dt.day, st_dt.hour])
    #
    print 'end the file; %s' % yymm
    
if __name__ == '__main__':
    run()
