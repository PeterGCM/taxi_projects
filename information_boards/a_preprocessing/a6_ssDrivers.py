import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import shiftProDur_dpath, shiftProDur_prefix
from information_boards import economicProfit_ap_dpath, economicProfit_ap_prefix
from information_boards import economicProfit_ns_dpath, economicProfit_ns_prefix
from information_boards import ssDriverTrip_dpath, ssDriverTrip_prefix
from information_boards import ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix
from information_boards import ssDriverEP_ap_dpath, ssDriverEP_ap_prefix
from information_boards import ssDriverEP_ns_dpath, ssDriverEP_ns_prefix
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv
#
logger = get_logger()


def run():
    for dpath in [ssDriverTrip_dpath, ssDriverShiftProDur_dpath, ssDriverEP_ap_dpath, ssDriverEP_ns_dpath]:
        check_dir_create(dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(10, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
                #             process_files(yymm)
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
    from traceback import format_exc
    try:
        logger.info('handle %s' % yymm)
        ssDrivers = load_pickle_file('%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yymm))
        #
        with open('%s/%s%s.csv' % (shiftProDur_dpath, shiftProDur_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix, yymm), 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in ssDrivers:
                        continue
                    writer.writerow(row)
        #
        yy, mm = yymm[:2], yymm[-2:]
        year, month = 2000 + int(yy), int(mm)
        with open('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (ssDriverTrip_dpath, ssDriverTrip_prefix, yymm), 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_headers = ['did', 'startTime', 'duration', 'fare', 'year', 'month', 'day', 'hour']
                writer.writerow(new_headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in ssDrivers:
                        continue
                    writer.writerow([row[hid['did']],
                                     row[hid['startTime']],
                                     row[hid['duration']],
                                     row[hid['fare']],
                                     year, month, row[hid['day']], row[hid['hour']]])
        #
        with open('%s/%s%s.csv' % (economicProfit_ap_dpath, economicProfit_ap_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (ssDriverEP_ap_dpath, ssDriverEP_ap_prefix, yymm),
                      'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in ssDrivers:
                        continue
                    writer.writerow(row)
        #
        with open('%s/%s%s.csv' % (economicProfit_ns_dpath, economicProfit_ns_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (ssDriverEP_ns_dpath, ssDriverEP_ns_prefix, yymm),
                      'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in ssDrivers:
                        continue
                    writer.writerow(row)
        logger.info('end %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()
