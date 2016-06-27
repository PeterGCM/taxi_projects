import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import IN, OUT
from b_aggregated_analysis.__init__ import logs_dir, log_prefix
from b_aggregated_analysis.__init__ import logs_last_day_dir, log_last_day_prefix
from b_aggregated_analysis.__init__ import ap_crossing_dir, ap_crossing_prefix
from b_aggregated_analysis.__init__ import ns_crossing_dir, ns_crossing_prefix
#
from taxi_common.file_handling_functions import get_all_files, save_pickle_file, remove_creat_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
#
def run():
    remove_creat_dir(ap_crossing_dir); remove_creat_dir(ns_crossing_dir)
    #
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
    print 'handle the file; %s' % yymm
    vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not = {}, {}
    vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not = {}, {}
    if yymm not in ['0901', '1001', '1011']:
        path_to_last_day_csv_file = None
        temp_csv_files = get_all_files(logs_last_day_dir, log_last_day_prefix, '.csv')
        prev_fn = None
        y, m = int(yymm[:2]), int(yymm[2:])
        prev_m = m - 1
        prev_yymm = '%02d%02d' %(y, prev_m)
        for temp_fn in temp_csv_files:
            if temp_fn.startswith('%s%s' % (log_last_day_prefix, prev_yymm)):
                prev_fn = temp_fn
                break
        assert prev_fn, yymm
        path_to_last_day_csv_file = '%s/%s' % (logs_last_day_dir, prev_fn)
        vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not, vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not = \
                        record_crossing_time(path_to_last_day_csv_file, vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not,
                                             vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not)
    path_to_csv_file = '%s/%s%s.csv' % (logs_dir, log_prefix, yymm)
    vehicle_ap_crossing_time_from_out_to_in, _, vehicle_ns_crossing_time_from_out_to_in, _ = \
            record_crossing_time(path_to_csv_file, vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not,
                                 vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not)
    #
    save_pickle_file('%s/%s%s.pkl' % (ap_crossing_dir, ap_crossing_prefix, yymm), vehicle_ap_crossing_time_from_out_to_in)
    save_pickle_file('%s/%s%s.pkl' % (ns_crossing_dir, ns_crossing_prefix, yymm), vehicle_ns_crossing_time_from_out_to_in)
    print 'end the file; %s' % yymm
    
def record_crossing_time(path_to_csv_file, vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not, vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not):
    with open(path_to_csv_file, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            t, vid = eval(row[hid['time']]), row[hid['vid']]
            ap_or_not, ns_or_not = eval(row[hid['ap-or-not']]), eval(row[hid['ns-or-not']])
            #
            if not vehicle_last_log_ap_or_not.has_key(vid):
                if ap_or_not == IN:
                    # the first log's position was occurred in the AP zone
                    assert not vehicle_ap_crossing_time_from_out_to_in.has_key(vid)
                    vehicle_ap_crossing_time_from_out_to_in[vid] = [t]
            else:
                assert vehicle_last_log_ap_or_not.has_key(vid)
                if vehicle_last_log_ap_or_not[vid] == OUT and eval(ap_or_not )== IN:
                    vehicle_ap_crossing_time_from_out_to_in.setdefault(vid, [t]).append(t)
            #
            if not vehicle_last_log_ns_or_not.has_key(vid):
                if ns_or_not == IN:
                    # the first log's position was occurred in the NS zone
                    assert not vehicle_ns_crossing_time_from_out_to_in.has_key(vid)
                    vehicle_ns_crossing_time_from_out_to_in[vid] = [t]
            else:
                assert vehicle_last_log_ns_or_not.has_key(vid)
                if vehicle_last_log_ns_or_not[vid] == OUT and ns_or_not == IN:
                    vehicle_ns_crossing_time_from_out_to_in.setdefault(vid, [t]).append(t)
            #        
            vehicle_last_log_ap_or_not[vid] = ap_or_not
            vehicle_last_log_ns_or_not[vid] = ns_or_not
    return vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not, vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not

if __name__ == '__main__':
    run()