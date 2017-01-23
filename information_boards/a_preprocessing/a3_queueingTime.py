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
    init_multiprocessor(6)
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
        with open(queueingTime_ap_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['did',
                           'startTime', 'endTime', 'duration', 'fare',
                           'tripMode', 'queueJoinTime', 'queueingTime',
                           'year', 'month', 'day', 'hour',
                           'pickUpTerminalAP', 'prevEndTerminalAP']
            writer.writerow(new_headers)
        with open(queueingTime_ns_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['did',
                           'startTime', 'endTime', 'duration', 'fare',
                           'tripMode', 'queueJoinTime', 'queueingTime',
                           'year', 'month', 'day', 'hour']
            writer.writerow(new_headers)
        #
        logger.info('start recording; %s' % yymm)
        with open('%s/Filtered-%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            for row in reader:
                did = row[hid['did']]
                et, duration = row[hid['endTime']], row[hid['duration']]
                fare = row[hid['fare']]
                year, month = row[hid['year']], row[hid['month']]
                day, hour = row[hid['day']], row[hid['hour']]
                pickUpTerminalAP, prevEndTerminalAP = row[hid['pickUpTerminalAP']], row[hid['prevEndTerminalAP']]
                #
                ap_tm, ns_tm = int(row[hid['tripModeAP']]), int(row[hid['tripModeNS']])
                vid, st, prev_tet = row[hid['vid']], eval(row[hid['startTime']]), eval(row[hid['prevTripEndTime']])
                #
                # Airport trip
                #
                if ap_tm != DIn_POut or ap_tm != DOut_POut:
                    queueing_time = None
                    if ap_tm == DIn_PIn:
                        queue_join_time = prev_tet
                        queueing_time = st - queue_join_time
                    elif ap_tm == DOut_PIn:
                        try:
                            i = bisect(crossingTime_ap[vid], st)
                            queue_join_time = crossingTime_ap[vid][i - 1] if i != 0 else crossingTime_ap[vid][0]
                            queueing_time = st - queue_join_time
                        except KeyError:
                            pass
                    if queueing_time != None and Q_LIMIT_MIN <= queueing_time:
                        new_row = [did,
                                   st, et, duration, fare,
                                   ap_tm, queue_join_time, queueing_time,
                                   year, month, day, hour,
                                   pickUpTerminalAP, prevEndTerminalAP]
                        append_record(queueingTime_ap_fpath, new_row)
                #
                # Night Safari
                #
                if ns_tm != DIn_POut or ns_tm != DOut_POut:
                    queueing_time = None
                    if ns_tm == DIn_PIn:
                        queue_join_time = prev_tet
                        queueing_time = st - queue_join_time
                    elif ns_tm == DOut_PIn:
                        try:
                            i = bisect(crossingTime_ns[vid], st)
                            queue_join_time = crossingTime_ns[vid][i - 1] if i != 0 else crossingTime_ns[vid][0]
                            queueing_time = st - queue_join_time
                        except KeyError:
                            pass
                    if queueing_time != None and Q_LIMIT_MIN <= queueing_time:
                        new_row = [did,
                                   st, et, duration, fare,
                                   ns_tm, queue_join_time, queueing_time,
                                   year, month, day, hour]
                        append_record(queueingTime_ns_fpath, new_row)
        logger.info('end the file; %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


def append_record(fpath, new_row):
    with open(fpath, 'a') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(new_row)


if __name__ == '__main__':
    run()
