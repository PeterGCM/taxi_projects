from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
import csv
from traceback import format_exc
#
from supports._setting import logs_dir, log_last_day_dir
from supports.etc_functions import get_all_files
from supports.handling_pkl import save_pickle_file
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports._setting import IN_AP, OUT_AP
from supports._setting import IN_NS, OUT_NS

def run():
    csv_files = get_all_files(logs_dir, '', '.csv')
    #
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
        try:
#             process_file(fn)
            put_task(process_file, [fn])
        except Exception as _:
            logging_msg('Algorithm runtime exception (%s)\n' % (fn) + format_exc())
            raise
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_file(fn):
    _, yymm = fn[:-len('.csv')].split('-')
    #
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not = {}, {}
    vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not = {}, {}
    if yymm not in ['0901', '1001', '1011']:
        path_to_last_day_csv_file = None
        temp_csv_files = get_all_files(log_last_day_dir, '', '.csv')
        prev_fn = None
        y, m = int(yymm[:2]), int(yymm[2:])
        prev_m = m - 1
        prev_yymm = '%02d%02d' %(y, prev_m)
        for temp_fn in temp_csv_files:
            if temp_fn.startswith('log-last-day-%s' % prev_yymm):
                prev_fn = temp_fn
                break
        assert prev_fn, yymm 
        path_to_last_day_csv_file = '%s/%s' % (log_last_day_dir, prev_fn) 
        vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not, vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not = \
                        record_crossing_time(path_to_last_day_csv_file, vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not,
                                             vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not)
    path_to_csv_file = '%s/%s' % (logs_dir, fn)
    vehicle_ap_crossing_time_from_out_to_in, _, vehicle_ns_crossing_time_from_out_to_in, _ = \
            record_crossing_time(path_to_csv_file, vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not,
                                 vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not)
    #
    save_pickle_file('%s/ap-crossing-time-%s.pkl' % (logs_dir, yymm), vehicle_ap_crossing_time_from_out_to_in)
    save_pickle_file('%s/ns-crossing-time-%s.pkl' % (logs_dir, yymm), vehicle_ns_crossing_time_from_out_to_in)
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
    
def record_crossing_time(path_to_csv_file, vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not, vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not):
    with open(path_to_csv_file, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_time, id_vid, id_did, id_ap_or_not, id_ns_or_not = headers.index('time'), headers.index('vid'), headers.index('did'), headers.index('ap-or-not'), headers.index('np-or-not')
        for row in reader:
            t, vid, _, ap_or_not, ns_or_not = eval(row[id_time]), row[id_vid], row[id_did], row[id_ap_or_not], row[id_ns_or_not]
            #
            if not vehicle_last_log_ap_or_not.has_key(vid):
                if ap_or_not == IN_AP:
                    # the first log's position was occurred in the AP zone
                    assert not vehicle_ap_crossing_time_from_out_to_in.has_key(vid)
                    vehicle_ap_crossing_time_from_out_to_in[vid] = [t]
            else:
                assert vehicle_last_log_ap_or_not.has_key(vid)
                if vehicle_last_log_ap_or_not[vid] == OUT_AP and ap_or_not == IN_AP:
                    vehicle_ap_crossing_time_from_out_to_in.setdefault(vid, [t]).append(t)
            #
            if not vehicle_last_log_ns_or_not.has_key(vid):
                if ns_or_not == IN_NS:
                    # the first log's position was occurred in the NS zone
                    assert not vehicle_ns_crossing_time_from_out_to_in.has_key(vid)
                    vehicle_ns_crossing_time_from_out_to_in[vid] = [t]
            else:
                assert vehicle_last_log_ns_or_not.has_key(vid)
                if vehicle_last_log_ns_or_not[vid] == OUT_NS and ns_or_not == IN_NS:
                    vehicle_ns_crossing_time_from_out_to_in.setdefault(vid, [t]).append(t)
            #        
            vehicle_last_log_ap_or_not[vid] = ap_or_not
            vehicle_last_log_ns_or_not[vid] = ns_or_not
    return vehicle_ap_crossing_time_from_out_to_in, vehicle_last_log_ap_or_not, vehicle_ns_crossing_time_from_out_to_in, vehicle_last_log_ns_or_not

if __name__ == '__main__':
    run()