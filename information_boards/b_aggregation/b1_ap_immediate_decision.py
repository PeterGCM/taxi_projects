import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import trip_ap_dp_flow_prefix, trip_ns_summary_fpath
from information_boards import NUM, DUR, FARE
from information_boards import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
#
from taxi_common.log_handling_functions import get_logger
from taxi_common.file_handling_functions import get_all_files
#
import pandas as pd
import csv
import time, datetime

logger = get_logger()


def run():
    def summary(write_fpath, read_fpath):
        logger.info('start the file; %s' % read_fpath.split('/')[-1])
        num_statistics = {}
        with open(read_fpath, 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
                cur_dt = datetime.datetime(year, month, day, hour)
                dow = cur_dt.strftime("%a")
                pickUpTerminalAP, prevEndTerminalAP = row[hid['pickUpTerminalAP']], row[hid['prevEndTerminalAP']]
                k = (year, month, day, dow, hour, pickUpTerminalAP, prevEndTerminalAP)
                if not num_statistics.has_key(k):
                    num_statistics[k] = 0
                num_statistics[k] += 1
        for (year, month, day, dow, hour, pickUpTerminalAP, prevEndTerminalAP), num in num_statistics.iteritems():
            with open(write_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([year, month, day, dow, hour, prevEndTerminalAP, pickUpTerminalAP, num])
        logger.info('end the file; %s' % read_fpath.split('/')[-1])
    #
    for y in xrange(9, 11):
        yyyy = str(2000 + y)
        yy = '%02d' % y
        logger.info('Start; %s' % yyyy)
        write_fpath = '%s/%s%s.csv' % (trip_dpath, trip_ap_dp_flow_prefix, yyyy)
        with open(write_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['year', 'month', 'day', 'dayOfWeek', 'hour', 'prevEndTerminalAP', 'pickUpTerminalAP', 'totalNum']
            writer.writerow(header)
        for fn in get_all_files(trip_dpath, '%s%s*' %(trip_prefix, yy)):
            read_fpath = '%s/%s' % (trip_dpath, fn)
            summary(write_fpath, read_fpath)


if __name__ == '__main__':
    run()
