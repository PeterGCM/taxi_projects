import __init__
#
'''

'''
#
from information_boards import statisticsAllDrivers_ap_dpath
from information_boards import statisticsAllDriversDay_ap_prefix, statisticsAllDriversMonth_ap_prefix, statisticsAllDriversTrip_ap_prefix
from information_boards import statisticsAllDrivers_ns_dpath
from information_boards import statisticsAllDriversDay_ns_prefix, statisticsAllDriversMonth_ns_prefix, statisticsAllDriversTrip_ns_prefix

from information_boards import statisticsSsDrivers_ap_dpath
from information_boards import statisticsSsDriversDay_ap_prefix, statisticsSsDriversMonth_ap_prefix, statisticsSsDriversTrip_ap_prefix
from information_boards import statisticsSsDrivers_ns_dpath
from information_boards import statisticsSsDriversDay_ns_prefix, statisticsSsDriversMonth_ns_prefix, statisticsSsDriversTrip_ns_prefix
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file, get_all_files
#
import csv


def run():
    for dpath in [statisticsSsDrivers_ap_dpath, statisticsSsDrivers_ns_dpath]:
        check_dir_create(dpath)
    #
    ssDrivers = set()
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data are corrupted
                continue
            ssDrivers = ssDrivers.union(load_pickle_file('%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yymm)))
    #
    for all_dpath, ss_dpath in [(statisticsAllDrivers_ap_dpath, statisticsSsDrivers_ap_dpath),
                                (statisticsAllDrivers_ns_dpath, statisticsSsDrivers_ns_dpath)]:
        for all_prefix, ss_prefix in [(statisticsAllDriversDay_ap_prefix, statisticsSsDriversDay_ap_prefix),
                                      (statisticsAllDriversDay_ns_prefix, statisticsSsDriversDay_ns_prefix),

                                      (statisticsAllDriversMonth_ap_prefix, statisticsSsDriversMonth_ap_prefix),
                                      (statisticsAllDriversMonth_ns_prefix, statisticsSsDriversMonth_ns_prefix),

                                      (statisticsAllDriversTrip_ap_prefix, statisticsSsDriversTrip_ap_prefix),
                                      (statisticsAllDriversTrip_ns_prefix, statisticsSsDriversTrip_ns_prefix),
                                      ]:
            for fn in get_all_files(all_dpath, '%s*' % all_prefix):
                period = fn[:-len('.csv')].split('-')[2]
                with open('%s/%s' % (all_dpath, fn), 'rt') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    header = reader.next()
                    hid = {h: i for i, h in enumerate(header)}
                    with open('%s/%s%s.csv' % (ss_dpath, ss_prefix, period), 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        writer.writerow(header)
                        for row in reader:
                            did = int(row[hid['driverID']])
                            if did not in ssDrivers:
                                continue
                            writer.writerow(row)


if __name__ == '__main__':
    run()
