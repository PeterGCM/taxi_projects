import __init__  # @UnresolvedImport # @UnusedImport
#
from init_project import DIn_PIn, DOut_PIn
from a_overall_analysis.__init__ import trips_dir, trip_prefix
from b_aggregated_analysis.__init__ import logs_dir, log_prefix
from b_aggregated_analysis.__init__ import ap_trips_dir, ap_trip_prefix
from b_aggregated_analysis.__init__ import ns_trips_dir, ns_trip_prefix
#
from taxi_common.file_handling_functions import get_all_files, load_picle_file, remove_creat_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
from bisect import bisect
#
def run():
    remove_creat_dir(airport_trips_dir); remove_creat_dir(nightsafari_trips_dir)
    csv_files = get_all_files(trips_dir, trip_prefix, '.csv')

    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data are corrupted
                continue
            # process_files(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1

def process_file(yymm):
    _, _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm 
    #
    ap_pkl_files = get_all_files(logs_dir, 'ap-crossing-time-', '.pkl')
    ap_pkl_file_path = None
    for pkl_fn in ap_pkl_files:
        _, _, _, pkl_yymm = pkl_fn[:-len('.pkl')].split('-')
        if pkl_yymm == yymm:
            ap_pkl_file_path = '%s/%s' % (logs_dir, pkl_fn)
            break
    else:
        assert False, yymm
    ap_crossing_times = load_picle_file(ap_pkl_file_path)
    #
    ns_pkl_files = get_all_files(logs_dir, 'ns-crossing-time-', '.pkl')
    ns_pkl_file_path = None
    for pkl_fn in ns_pkl_files:
        _, _, _, pkl_yymm = pkl_fn[:-len('.pkl')].split('-')
        if pkl_yymm == yymm:
            ns_pkl_file_path = '%s/%s' % (logs_dir, pkl_fn)
            break
    else:
        assert False, yymm
    ns_crossing_times = load_picle_file(ns_pkl_file_path)
    #
    init_csv_files(yymm)
    
    with open('%s/%s' % (trips_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        header_id = {h : i for i, h in enumerate(headers)}
        for row in reader:
            tid, did = row[header_id['tid']], row[header_id['did']]
            et, duration = row[header_id['end-time']], row[header_id['duration']]
            fare = row[header_id['fare']]
            #
            ap_tm, ns_tm = int(row[header_id['ap-trip-mode']]), int(row[header_id['ns-trip-mode']]) 
            vid, st, prev_tet = row[header_id['vid']], eval(row[header_id['start-time']]), eval(row[header_id['prev-trip-end-time']])
            #
            is_ap_trip, is_ns_trip = False, False 
            #
            if ap_tm == DInAP_PInAP:
                is_ap_trip = True
                ap_join_queue_time = prev_tet
            elif ap_tm == DOutAP_PInAP:
                is_ap_trip = True
                try:
                    i = bisect(ap_crossing_times[vid], st)
                except KeyError:
                    print '%s-tid-%s' % (yymm, row[header_id['tid']])
                    continue
                ap_join_queue_time = ap_crossing_times[vid][i - 1] if i != 0 else ap_crossing_times[vid][0]
            if is_ap_trip:
                with open('%s/%s%s.csv' % (airport_trips_dir, ap_trip_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    ap_queue_time = st - ap_join_queue_time
                    new_row = [tid, vid, did, st, et, duration, fare, prev_tet,
                                ap_tm, ap_join_queue_time, ap_queue_time]
                    writer.writerow(new_row)
            #
            if ns_tm == DInNS_PInNS:
                is_ns_trip = True
                ns_join_queue_time = prev_tet
            elif ns_tm == DOutNS_PInNS:
                is_ns_trip = True
                try:
                    i = bisect(ns_crossing_times[vid], st)
                except KeyError:
                    print '%s-tid-%s' % (yymm, row[header_id['tid']])
                    continue
                ns_join_queue_time = ns_crossing_times[vid][i - 1] if i != 0 else ns_crossing_times[vid][0]
            if is_ns_trip:
                with open('%s/%s%s.csv' % (nightsafari_trips_dir, ns_trip_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    ns_queue_time = st - ns_join_queue_time
                    new_row = [tid, vid, did, st, et, duration, fare, prev_tet,
                                ns_tm, ns_join_queue_time, ns_queue_time]
                    writer.writerow(new_row)        
    print 'end the file; %s' % yymm 

def init_csv_files(yymm):
    with open('%s/%s%s.csv' % (airport_trips_dir, ap_trip_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['tid', 'vid', 'did',
                           'start-time', 'end-time', 'duration',
                           'fare', 'prev-trip-end-time',
                           'ap-trip-mode', 'ap-join-queue-time', 'ap-queue-time', ]
            writer.writerow(new_headers)
    #
    with open('%s/%s%s.csv' % (nightsafari_trips_dir, ns_trip_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['tid', 'vid', 'did',
                           'start-time', 'end-time', 'duration',
                           'fare', 'prev-trip-end-time',
                           'ns-trip-mode', 'ns-join-queue-time', 'ns-queue-time']
            writer.writerow(new_headers)
         
if __name__ == '__main__':
    run()
