#
import csv

from information_boards import IN, OUT
from information_boards.old_codes.b_aggregated_analysis import ap_crossing_dir, ap_crossing_prefix
from information_boards.old_codes.b_aggregated_analysis import logs_dir, log_prefix
from information_boards.old_codes.b_aggregated_analysis import logs_last_day_dir, log_last_day_prefix
from information_boards.old_codes.b_aggregated_analysis import ns_crossing_dir, ns_crossing_prefix
from taxi_common.file_handling_functions import get_all_files, save_pickle_file, check_dir_create, check_path_exist
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor


def run():
    check_dir_create(ap_crossing_dir); check_dir_create(ns_crossing_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data are corrupted
                continue
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    ap_pkl_fpath = '%s/%s%s.pkl' % (ap_crossing_dir, ap_crossing_prefix, yymm)
    ns_pkl_fpath = '%s/%s%s.pkl' % (ns_crossing_dir, ns_crossing_prefix, yymm)
    if check_path_exist(ap_pkl_fpath) and check_path_exist(ns_pkl_fpath):
        return None
    print 'handle the file; %s' % yymm
    veh_ap_crossing_time, veh_last_log_ap_or_not = {}, {}
    veh_ns_crossing_time, veh_last_log_ns_or_not = {}, {}
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
        # if (time.time() - get_created_time(path_to_last_day_csv_file)) < HOUR1:
        #     return None
        veh_ap_crossing_time, veh_last_log_ap_or_not, veh_ns_crossing_time, veh_last_log_ns_or_not = \
                        record_crossing_time(path_to_last_day_csv_file, veh_ap_crossing_time, veh_last_log_ap_or_not,
                                             veh_ns_crossing_time, veh_last_log_ns_or_not)
    path_to_csv_file = '%s/%s%s.csv' % (logs_dir, log_prefix, yymm)
    veh_ap_crossing_time, _, veh_ns_crossing_time, _ = \
            record_crossing_time(path_to_csv_file, veh_ap_crossing_time, veh_last_log_ap_or_not,
                                 veh_ns_crossing_time, veh_last_log_ns_or_not)
    #
    save_pickle_file(ap_pkl_fpath, veh_ap_crossing_time)
    save_pickle_file(ns_pkl_fpath, veh_ns_crossing_time)
    print 'end the file; %s' % yymm


def record_crossing_time(path_to_csv_file, veh_ap_crossing_time, veh_last_log_ap_or_not, veh_ns_crossing_time, veh_last_log_ns_or_not):
    with open(path_to_csv_file, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            t, vid = eval(row[hid['time']]), row[hid['vid']]
            ap_or_not, ns_or_not = eval(row[hid['ap-or-not']]), eval(row[hid['ns-or-not']])
            #
            if not veh_last_log_ap_or_not.has_key(vid):
                if ap_or_not == IN:
                    # the first log's position was occurred in the AP zone
                    assert not veh_ap_crossing_time.has_key(vid)
                    veh_ap_crossing_time[vid] = [t]
            else:
                assert veh_last_log_ap_or_not.has_key(vid)
                if veh_last_log_ap_or_not[vid] == OUT and ap_or_not== IN:
                    veh_ap_crossing_time.setdefault(vid, [t]).append(t)
            #
            if not veh_last_log_ns_or_not.has_key(vid):
                if ns_or_not == IN:
                    # the first log's position was occurred in the NS zone
                    assert not veh_ns_crossing_time.has_key(vid)
                    veh_ns_crossing_time[vid] = [t]
            else:
                assert veh_last_log_ns_or_not.has_key(vid)
                if veh_last_log_ns_or_not[vid] == OUT and ns_or_not == IN:
                    veh_ns_crossing_time.setdefault(vid, [t]).append(t)
            #        
            veh_last_log_ap_or_not[vid] = ap_or_not
            veh_last_log_ns_or_not[vid] = ns_or_not
    return veh_ap_crossing_time, veh_last_log_ap_or_not, veh_ns_crossing_time, veh_last_log_ns_or_not

if __name__ == '__main__':
    run()