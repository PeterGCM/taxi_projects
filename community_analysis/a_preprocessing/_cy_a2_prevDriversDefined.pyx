import __init__
#
'''

'''
#
from community_analysis import ss_trips_dpath, ss_trips_prefix
from community_analysis import prevDriversDefined_dpath, prevDriversDefined_prefix
from community_analysis import driversRelations_fpaths
from community_analysis import HISTORY_LOOKUP_LENGTH, MINUTES40
#
from taxi_common._classes import zone, driver
from taxi_common.sg_grid_zone import get_sg_zones
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, get_all_files, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
import pandas as pd
import numpy as np
#
logger = get_logger()


def run(yymm):
    check_dir_create(prevDriversDefined_dpath)
    # process_month(yymm)
    #
    # init_multiprocessor(11)
    # count_num_jobs = 0
    # for y in range(12, 13):
    #     for m in range(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         if yymm in ['0912', '1010']:
    #             continue
    #         # process_month(yymm)
    #         put_task(process_month, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)
    filtering('2009')
    find_driversRelations('2009')


def find_driversRelations(year):
    yy = year[2:]
    driversRelations = {}
    for fn in get_all_files(prevDriversDefined_dpath, 'Filtered-%s%s*' % (prevDriversDefined_prefix, yy)):
        logger.info('handle the file; %s' % fn)
        with open('%s/%s' % (prevDriversDefined_dpath, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did1 = int(row[hid['did']])
                prevDrivers = row[hid['prevDrivers']].split('&')
                if len(prevDrivers) == 1 and prevDrivers[0] == '':
                    continue
                if not driversRelations.has_key(did1):
                    driversRelations[did1] = set()
                for did0 in map(int, prevDrivers):
                    driversRelations[did1].add(did0)
    save_pickle_file(driversRelations_fpaths[year], driversRelations)


def process_month(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        ss_trips_fpath = '%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, yymm)
        if not check_path_exist(ss_trips_fpath):
            logger.info('The file X exists; %s' % yymm)
            return None
        prevDriversDefined_fpath = '%s/%s%s.csv' % (prevDriversDefined_dpath, prevDriversDefined_prefix, yymm)
        if check_path_exist(prevDriversDefined_fpath):
            logger.info('The processed; %s' % yymm)
            return None
        drivers = {}
        zones = generate_zones()
        handling_day = 0
        with open(prevDriversDefined_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['did',
                             'timeFrame', 'zi', 'zj',
                             'time', 'day', 'month',
                             'start-long', 'start-lat',
                             'distance', 'duration', 'fare',
                             'spendingTime', 'prevDrivers'])
            with open(ss_trips_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
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
                    prevDrivers = drivers[did].find_prevDriver(t, z)
                    writer.writerow(row + ['&'.join(map(str, prevDrivers))])
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise

class ca_zone(zone):
    def __init__(self, boundary_relation_with_poly, zi, zj, cCoor_gps, polyPoints_gps):
        zone.__init__(self, boundary_relation_with_poly, zi, zj, cCoor_gps, polyPoints_gps)
        self.logQ = []

    def add_driver_in_logQ(self, t, d):
        self.logQ.append([t, d])

    def update_logQ(self, t):
        while self.logQ and self.logQ[0] < t - HISTORY_LOOKUP_LENGTH:
            self.logQ.pop(0)

    def init_logQ(self):
        self.logQ = []

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


def generate_zones():
    zones = {}
    basic_zones = get_sg_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = ca_zone(z.relation_with_poly, z.zi, z.zj, z.cCoor_gps, z.polyPoints_gps)
    return zones


def filtering(year):
    yy = year[2:]
    for fn in get_all_files(prevDriversDefined_dpath, '%s%s*' % (prevDriversDefined_prefix, yy)):
        df = pd.read_csv('%s/%s' % (prevDriversDefined_dpath, fn))
        cn = 'spendingTime'
        outlier_set = set(np.where(df[cn] > MINUTES40)[0].tolist())
        df = df.drop(df.index[list(outlier_set)])
        df.to_csv('%s/Filtered-%s' % (prevDriversDefined_dpath, fn), index=False)


if __name__ == '__main__':
    run()
