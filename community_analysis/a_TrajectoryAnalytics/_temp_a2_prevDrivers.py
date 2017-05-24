import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import HISTORY_LOOKUP_LENGTH, MINUTES40
#
from taxi_common._classes import zone, driver
from taxi_common.sg_grid_zone import get_sg_zones
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, get_all_files, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime
import pandas as pd
import numpy as np
#
logger = get_logger()

if_dpath = dpaths['driverTrip']
if_prefix = prefixs['driverTrip']

#



def run(yymm):
    process_month(yymm)


def process_month(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        ifpath = '%s/%s%s.csv' % (if_dpath, if_prefix, yymm)
        if not check_path_exist(ifpath):
            logger.info('The file X exists; %s' % yymm)
            return None
        ofpath = '%s/prevDrivers-%s%s.csv' % (if_dpath, if_prefix, yymm)
        # if check_path_exist(ofpath):
        #     logger.info('The processed; %s' % yymm)
        #     return None
        drivers = {}
        zones = generate_zones()
        handling_day = 0
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            with open(ofpath, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_header = header + ['prevDrivers']
                writer.writerow(new_header)
                for row in reader:
                    t = eval(row[hid['time']])
                    cur_dt = datetime.datetime.fromtimestamp(t)
                    if handling_day != cur_dt.day:
                        logger.info('Processing %s %dth day (month %d)' % (yymm, cur_dt.day, cur_dt.month))
                        handling_day = cur_dt.day
                    did = int(row[hid['did']])
                    zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                    try:
                        z = zones[(zi, zj)]
                    except KeyError:
                        continue
                    if not drivers.has_key(did):
                        drivers[did] = ca_driver_withPrevDrivers(did)
                    if did == 1 and t == eval('1233723600'):
                        print 'hi'


                    prevDrivers = drivers[did].find_prevDriver(t, z)
                    writer.writerow(row + ['&'.join(map(str, prevDrivers))])
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


class ca_driver_withPrevDrivers(driver):
    def __init__(self, did):
        driver.__init__(self, did)

    def find_prevDriver(self, t, z):
        z.update_logQ(t)
        prevDrivers = set()
        for _, d in z.logQ:
            if d.did == self.did:
                continue
            prevDrivers.add(d.did)
        z.add_driver_in_logQ(t, self)
        return prevDrivers


class ca_zone(zone):
    def __init__(self, boundary_relation_with_poly, zi, zj, cCoor_gps, polyPoints_gps):
        zone.__init__(self, boundary_relation_with_poly, zi, zj, cCoor_gps, polyPoints_gps)
        self.logQ = []

    def add_driver_in_logQ(self, t, d):
        self.logQ.append([t, d])

    def update_logQ(self, t):
        while self.logQ and self.logQ[0][0] < t - HISTORY_LOOKUP_LENGTH:
            self.logQ.pop(0)

    def init_logQ(self):
        self.logQ = []


def generate_zones():
    zones = {}
    basic_zones = get_sg_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = ca_zone(z.relation_with_poly, z.zi, z.zj, z.cCoor_gps, z.polyPoints_gps)
    return zones

if __name__ == '__main__':
    run('0902')
