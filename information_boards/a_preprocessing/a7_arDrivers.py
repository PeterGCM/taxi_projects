import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import shiftProDur_dpath, shiftProDur_prefix
from information_boards import economicProfit_ap_dpath, economicProfit_ap_prefix
from information_boards import economicProfit_ns_dpath, economicProfit_ns_prefix
from information_boards import arDriver_dpath
from information_boards import arDriver2009_ap_fpath, arDriver2010_ap_fpath
from information_boards import arDriver2009_ns_fpath, arDriver2010_ns_fpath
from information_boards import arDriverTrip_dpath, arDriverTrip_prefix
from information_boards import arDriverShiftProDur_dpath, arDriverShiftProDur_prefix
from information_boards import arDriverEP_ap_dpath, arDriverEP_ap_prefix
from information_boards import arDriverEP_ns_dpath, arDriverEP_ns_prefix
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, save_pickle_file, get_fn_only, load_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import csv

logger = get_logger()


def run():
    for dpath in [arDriver_dpath]:
        check_dir_create(dpath)
    #
    find_arDriver()


def find_arDriver():
    for y, pkl_fpath, loc_dpath, loc_prefix in [(9, arDriver2009_ap_fpath, economicProfit_ap_dpath, economicProfit_ap_prefix),
                                    (10, arDriver2010_ap_fpath, economicProfit_ap_dpath, economicProfit_ap_prefix),
                                    (9, arDriver2009_ns_fpath, economicProfit_ns_dpath, economicProfit_ns_prefix),
                                    (10, arDriver2010_ns_fpath, economicProfit_ns_dpath, economicProfit_ns_prefix)]:
        logger.info('handle %s' % get_fn_only(pkl_fpath))
        driver_month_counting = {}
        month_fns = get_all_files(loc_dpath, '%s%02d*' % (loc_prefix, y))
        for fn in month_fns:
            df = pd.read_csv('%s/%s' % (loc_dpath, fn))
            for did in set(df['did']):
                if not driver_month_counting.has_key(did):
                    driver_month_counting[did] = 0
                driver_month_counting[did] += 1
        save_pickle_file(pkl_fpath, [did for did, month_counting in driver_month_counting.iteritems()
                                     if month_counting == len(month_fns)])


def process_files(yymm):
    from traceback import format_exc
    try:
        logger.info('handle %s' % yymm)
        yy = int(yymm[:2])

        ap_fn = get_all_files(arDriver_dpath, '*%s-ap.pkl')[0]
        ns_fn = get_all_files(arDriver_dpath, '*%s-ns.pkl')[0]
        arDrivers_ap = load_pickle_file('%s/%s' % (arDriver_dpath, ap_fn))
        arDrivers_ns = load_pickle_file('%s/%s' % (arDriver_dpath, ns_fn))
        #
        with open('%s/%s%s.csv' % (shiftProDur_dpath, shiftProDur_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (arDriverShiftProDur_dpath, arDriverShiftProDur_prefix, yymm), 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in arDrivers_ap + arDrivers_ns:
                        continue
                    writer.writerow(row)
        #
        yy, mm = yymm[:2], yymm[-2:]
        year, month = 2000 + int(yy), int(mm)
        with open('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (arDriverTrip_dpath, arDriverTrip_prefix, yymm), 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_headers = ['did', 'startTime', 'duration', 'fare', 'year', 'month', 'day', 'hour']
                writer.writerow(new_headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in arDrivers_ap + arDrivers_ns:
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
            with open('%s/%s%s.csv' % (arDriverEP_ap_dpath, arDriverEP_ap_prefix, yymm),
                      'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in arDrivers_ap:
                        continue
                    writer.writerow(row)
        #
        with open('%s/%s%s.csv' % (economicProfit_ns_dpath, economicProfit_ns_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (arDriverEP_ns_dpath, arDriverEP_ns_prefix, yymm),
                      'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(headers)
                for row in reader:
                    did = int(row[hid['did']])
                    if did not in arDrivers_ns:
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
