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
from information_boards import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from information_boards import Q_LIMIT_MIN
#
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create, check_path_exist
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
from bisect import bisect
import csv

logger = get_logger()


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
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        queueingTime_ap_fpath = '%s/%s%s.csv' % (queueingTime_ap_dpath, queueingTime_ap_prefix, yymm)
        queueingTime_ns_fpath = '%s/%s%s.csv' % (queueingTime_ns_dpath, queueingTime_ns_prefix, yymm)
        if check_path_exist(queueingTime_ap_fpath) and check_path_exist(queueingTime_ns_fpath):
            logger.info('The file had already been processed; %s' % yymm)
            return
        #
        logger.info('load pickle files; %s' % yymm)
        ap_pkl_fpath = '%s/%s%s.pkl' % (crossingTime_ap_dpath, crossingTime_ap_prefix, yymm)
        ns_pkl_fpath = '%s/%s%s.pkl' % (crossingTime_ns_dpath, crossingTime_ns_prefix, yymm)
        crossingTime_ap, crossingTime_ns = load_pickle_file(ap_pkl_fpath), load_pickle_file(ns_pkl_fpath)
        #
        logger.info('initiate csv files; %s' % yymm)
        for fpath in [queueingTime_ap_fpath, queueingTime_ns_fpath]:
            with open(fpath, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_headers = ['did',
                                   'startTime', 'endTime', 'duration', 'fare',
                                   'tripMode', 'queueJoinTime', 'queueingTime', 'day', 'hour']
                    writer.writerow(new_headers)
        #
        logger.info('start recording; %s' % yymm)
        with open('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            for row in reader:
                did = row[hid['did']]
                et, duration = row[hid['endTime']], row[hid['duration']]
                fare = row[hid['fare']]
                #
                ap_tm, ns_tm = int(row[hid['tripModeAP']]), int(row[hid['tripModeNS']])
                vid, st, prev_tet = row[hid['vid']], eval(row[hid['startTime']]), eval(row[hid['prevTripEndTime']])
                #
                for tm, crossingTime, fpath in [(ap_tm, crossingTime_ap, queueingTime_ap_fpath),
                                                                 (ns_tm, crossingTime_ns, queueingTime_ns_fpath)]:
                    if tm == DIn_POut or tm == DOut_POut:
                        continue
                    if tm == DIn_PIn:
                        queue_join_time = prev_tet
                    elif tm == DOut_PIn:
                        try:
                            i = bisect(crossingTime[vid], st)
                        except KeyError:
                            continue
                        queue_join_time = crossingTime[vid][i - 1] if i != 0 else crossingTime[vid][0]
                    queueing_time = st - queue_join_time
                    if queueing_time < Q_LIMIT_MIN:
                        continue
                    day, hour = row[hid['day']], row[hid['hour']]
                    with open(fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [did,
                                   st, et, duration, fare,
                                   tm, queue_join_time, queueing_time, day, hour]
                        writer.writerow(new_row)
        logger.info('end the file; %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise
    
if __name__ == '__main__':
    run()
