import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import crossingTime_ap_dpath, crossingTime_ap_prefix
from information_boards import crossingTime_ns_dpath, crossingTime_ns_prefix
from information_boards import queueingTime_ap_dpath, queueingTime_ap_prefix
from information_boards import queueingTime_ns_dpath, queueingTime_ns_prefix
#



from information_boards import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from information_boards import Q_LIMIT_MIN



from taxi_common.file_handling_functions import load_pickle_file, check_dir_create, check_path_exist
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
from bisect import bisect
import csv



def run():
    for dpath in [queueingTime_ap_dpath, queueingTime_ns_dpath]:
        check_dir_create(dpath)
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
    ap_pkl_fpath = '%s/%s%s.pkl' % (crossingTime_ap_dpath, crossingTime_ap_prefix, yymm)
    ns_pkl_fpath = '%s/%s%s.pkl' % (crossingTime_ns_dpath, crossingTime_ns_prefix, yymm)
    if not (check_path_exist(ap_pkl_fpath) and check_path_exist(ns_pkl_fpath)):
        return None
    #
    # Load pickle files
    #
    crossingTime_ap, crossingTime_ns = load_pickle_file(ap_pkl_fpath), load_pickle_file(ns_pkl_fpath)
    #
    # Initiate csv files
    #
    ap_trip_fpath = '%s/%s%s.csv' % (queueingTime_ap_dpath, queueingTime_ap_prefix, yymm)
    ns_trip_fpath = '%s/%s%s.csv' % (queueingTime_ns_dpath, queueingTime_ns_prefix, yymm)
    if check_path_exist(ap_trip_fpath) and check_path_exist(ns_trip_fpath):
        return None
    print 'handle the file; %s' % yymm
    for fpath in [ap_trip_fpath, ns_trip_fpath]:
        with open(fpath, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_headers = ['tid', 'vid', 'did',
                               'start-time', 'end-time', 'duration',
                               'fare', 'prevTripEndTime',
                               'tripMode', 'queueJoinTime', 'queueingTime']
                writer.writerow(new_headers)
    #
    with open('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        for row in reader:
            tid, did = row[hid['tid']], row[hid['did']]
            et, duration = row[hid['end-time']], row[hid['duration']]
            fare = row[hid['fare']]
            #
            ap_tm, ns_tm = int(row[hid['ap-trip-mode']]), int(row[hid['ns-trip-mode']]) 
            vid, st, prev_tet = row[hid['vid']], eval(row[hid['start-time']]), eval(row[hid['prev-trip-end-time']])
            #
            for tm, crossing_time, fpath in [(ap_tm, crossingTime_ap, ap_trip_fpath),
                                                             (ns_tm, crossingTime_ns, ns_trip_fpath)]:
                if tm == DIn_POut or tm == DOut_POut:
                    continue
                if tm == DIn_PIn:
                    queue_join_time = prev_tet
                elif tm == DOut_PIn:
                    try:
                        i = bisect(crossing_time[vid], st)
                    except KeyError:
                        print '%s-tid-%s' % (yymm, row[hid['tid']])
                        continue
                    queue_join_time = crossing_time[vid][i - 1] if i != 0 else crossing_time[vid][0]
                with open(fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    queueing_time = st - queue_join_time
                    if queueing_time < Q_LIMIT_MIN:
                        queueing_time = Q_LIMIT_MIN
                    new_row = [tid, vid, did, st, et, duration, fare, prev_tet,
                                tm, queue_join_time, queueing_time]
                    writer.writerow(new_row)
    print 'end the file; %s' % yymm 
    
if __name__ == '__main__':
    run()
