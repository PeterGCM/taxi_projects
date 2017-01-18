import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import trip_ap_summary_fpath, trip_ns_summary_fpath
from information_boards import NUM, DUR, FARE
from information_boards import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
#
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import csv
import time, datetime

logger = get_logger()


def run():
    def summary(yymm):
        logger.info('start the file; %s' % yymm)
        year, month = 2000 + int(yymm[:2]), int(yymm[2:])
        num_statistics = {}
        with open('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                day, hour = int(row[hid['day']]), int(row[hid['hour']])
                cur_dt = datetime.datetime(year, month, day, hour)
                dow = cur_dt.strftime("%a")
                pickUpTerminalAP, prevEndTerminalAP = row[hid['pickUpTerminalAP']], row[hid['prevEndTerminalAP']]
                k = (year, month, day, dow, hour, pickUpTerminalAP, prevEndTerminalAP)
                if not num_statistics.has_key(k):
                    num_statistics[k] = 0
                num_statistics[k] += 1
        for (year, month, day, dow, hour, pickUpTerminalAP, prevEndTerminalAP), num in num_statistics.iteritems():
            with open(trip_ap_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([year, month, day, dow, hour, pickUpTerminalAP, prevEndTerminalAP, num])
        logger.info('end the file; %s' % yymm)
    #
    logger.info('Start')
    with open(trip_ap_summary_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['year', 'month', 'day', 'dayOfWeek', 'hour', 'pickUpTerminalAP', 'prevEndTerminalAP', 'totalNum']
        writer.writerow(header)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            summary(yymm)


if __name__ == '__main__':
    run()
