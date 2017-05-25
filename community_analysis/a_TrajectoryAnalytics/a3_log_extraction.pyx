import __init__
#
from community_analysis import FRI, SAT, SUN
from community_analysis import AM10, PM8
from community_analysis import taxi_home
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime

logger = get_logger()

of_dpath = dpaths['driverLog']
of_prefixs = prefixs['driverLog']

try:
    check_dir_create(of_dpath)
except OSError:
    pass


def get_driver_log(yymm, did):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        yy, mm = yymm[:2], yymm[2:]
        log_fpath = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm)
        ofpath = None
        handling_day = 0
        with open(log_fpath, 'rb') as logFile:
            logReader = csv.reader(logFile)
            logHeader = logReader.next()
            hidL = {h: i for i, h in enumerate(logHeader)}
            for row in logReader:
                didL = int(row[hidL['driver-id']])
                if didL != did:
                    continue
                t = eval(row[hidL['time']])
                cur_dtL = datetime.datetime.fromtimestamp(t)
                if cur_dtL.weekday() in [FRI, SAT, SUN]:
                    continue
                if cur_dtL.hour < AM10:
                    continue
                if PM8 <= cur_dtL.hour:
                    continue
                if handling_day != cur_dtL.day:
                    handling_day = cur_dtL.day
                    ofpath = '%s/%s%s%02d-%d.csv' % (of_dpath, of_prefixs, yymm, handling_day, did)
                    with open(ofpath, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow(logHeader)
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


def get_drivers_log(yymm, drivers):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        yy, mm = yymm[:2], yymm[2:]
        log_fpath = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm)
        handling_day = 0
        with open(log_fpath, 'rb') as logFile:
            logReader = csv.reader(logFile)
            logHeader = logReader.next()
            hidL = {h: i for i, h in enumerate(logHeader)}
            dl_fpath = {}
            for row in logReader:
                didL = int(row[hidL['driver-id']])
                if didL not in drivers:
                    continue
                t = eval(row[hidL['time']])
                cur_dtL = datetime.datetime.fromtimestamp(t)
                if cur_dtL.weekday() in [FRI, SAT, SUN]:
                    continue
                if cur_dtL.hour < AM10:
                    continue
                if PM8 <= cur_dtL.hour:
                    continue
                if handling_day != cur_dtL.day:
                    handling_day = cur_dtL.day
                    for did in drivers:
                        dl_fpath[did] = '%s/%s%s%02d-%d.csv' % (of_dpath, of_prefixs, yymm, handling_day, did)
                        with open(dl_fpath[did], 'wt') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow(logHeader)
                with open(dl_fpath[didL], 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    get_driver_log('0901', 1)