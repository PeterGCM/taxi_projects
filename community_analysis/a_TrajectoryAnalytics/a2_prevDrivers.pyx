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

if_dpath = dpaths['roamingNinterTravel']
if_prefixs = prefixs['roamingNinterTravel']
#
of_dpath = dpaths['prevDrivers']
of_prefixs = prefixs['prevDrivers']

try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(yymm):
    process_month(yymm)
    # filtering('2012')
    # find_driversRelations('2012')


def roamingTimeFiltering(year):
    from traceback import format_exc
    try:
        logger.info('start filtering')
        fs_fpath = '%s/roamingTimeFiltered-summary-%s%s.csv' % (of_dpath, of_prefixs, year)
        with open(fs_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['yymm', 'numTrips', 'numLessThanZero', 'numMoreThan40MIN', 'numFilteredTrips']
            writer.writerow(header)
        yy = year[2:]
        for fn in get_all_files(of_dpath, '%s%s*' % (of_prefixs, yy)):
            new_fpath = '%s/roamingTimeFiltered-%s' % (of_dpath, fn)
            if check_path_exist(new_fpath):
                continue
            _, yymm = fn[:-len('.csv')].split('-')
            df = pd.read_csv('%s/%s' % (of_dpath, fn))
            numTrips = len(df)
            cn = 'roamingTime'
            outlier_set = set(np.where(df[cn] < 0)[0].tolist())
            numLessThanZero = len(outlier_set)
            outlier_set = outlier_set.union(set(np.where(df[cn] > MINUTES40)[0].tolist()))
            numMoreThan40MIN = len(outlier_set) - numLessThanZero
            numFilteredTrips = numLessThanZero + numMoreThan40MIN
            df = df.drop(df.index[list(outlier_set)])
            df = df.drop(['interTravelTime'], axis=1)
            df.to_csv(new_fpath, index=False)
            with open(fs_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = [yymm, numTrips, numLessThanZero, numMoreThan40MIN, numFilteredTrips]
                writer.writerow(new_row)
        driversRelations = {}
        superSet_fpath = '%s/roamingTimeFiltered-superSet-%s%s.pkl' % (of_dpath, of_prefixs, year)
        logger.info('handle the file; %s' % superSet_fpath)
        for fn in get_all_files(of_dpath, 'roamingTimeFiltered-%s%s*' % (of_prefixs, yy)):
            logger.info('handle the file; %s' % fn)
            with open('%s/%s' % (of_dpath, fn), 'rb') as r_csvfile:
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
        save_pickle_file(superSet_fpath, driversRelations)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], year), 'w') as f:
            f.write(format_exc())


def interTravelTimeFiltering(year):
    from traceback import format_exc
    try:
        logger.info('start filtering')
        fs_fpath = '%s/interTravelTimeFiltered-summary-%s%s.csv' % (of_dpath, of_prefixs, year)
        with open(fs_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['yymm', 'numTrips', 'numLessThanZero', 'Per95Value', 'numMoreThanPer95Value', 'numFilteredTrips']
            writer.writerow(header)
        yy = year[2:]
        for fn in get_all_files(of_dpath, '%s%s*' % (of_prefixs, yy)):
            new_fpath = '%s/interTravelTimeFiltered-%s' % (of_dpath, fn)
            if check_path_exist(new_fpath):
                continue
            _, yymm = fn[:-len('.csv')].split('-')
            df = pd.read_csv('%s/%s' % (of_dpath, fn))
            numTrips = len(df)
            cn = 'interTravelTime'
            outlier_set = set(np.where(df[cn] < 0)[0].tolist())
            numLessThanZero = len(outlier_set)
            per95Value = df[cn].quantile(0.95)
            outlier_set = outlier_set.union(set(np.where(df[cn] > per95Value)[0].tolist()))
            numMoreThanPer95Value = len(outlier_set) - numLessThanZero
            numFilteredTrips = numLessThanZero + numMoreThanPer95Value
            df = df.drop(df.index[list(outlier_set)])
            df = df.drop(['roamingTime'], axis=1)
            df.to_csv(new_fpath, index=False)
            with open(fs_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = [yymm, numTrips, numLessThanZero, per95Value, numMoreThanPer95Value, numFilteredTrips]
                writer.writerow(new_row)
        driversRelations = {}
        superSet_fpath = '%s/interTravelTimeFiltered-superSet-%s%s.pkl' % (of_dpath, of_prefixs, year)
        logger.info('handle the file; %s' % superSet_fpath)
        for fn in get_all_files(of_dpath, 'interTravelTimeFiltered-%s%s*' % (of_prefixs, yy)):
            logger.info('handle the file; %s' % fn)
            with open('%s/%s' % (of_dpath, fn), 'rb') as r_csvfile:
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
        save_pickle_file(superSet_fpath, driversRelations)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], year), 'w') as f:
            f.write(format_exc())


def process_month(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        ifpath = '%s/%s%s.csv' % (if_dpath, if_prefixs, yymm)
        if not check_path_exist(ifpath):
            logger.info('The file X exists; %s' % yymm)
            return None
        ofpath = '%s/%s%s.csv' % (of_dpath, of_prefixs, yymm)
        if check_path_exist(ofpath):
            logger.info('The processed; %s' % yymm)
            return None
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

# 
# def filtering(year):
#     yy = year[2:]
#     for fn in get_all_files(prevDriversDefined_dpath, '%s%s*' % (prevDriversDefined_prefix, yy)):
#         df = pd.read_csv('%s/%s' % (prevDriversDefined_dpath, fn))
#         cn = 'roamingTime'
#         outlier_set = set(np.where(df[cn] > MINUTES40)[0].tolist())
#         df = df.drop(df.index[list(outlier_set)])
#         df.to_csv('%s/Filtered-%s' % (prevDriversDefined_dpath, fn), index=False)
# 
# 
# def find_driversRelations(year):
#     yy = year[2:]
#     driversRelations = {}
#     for fn in get_all_files(prevDriversDefined_dpath, 'Filtered-%s%s*' % (prevDriversDefined_prefix, yy)):
#         logger.info('handle the file; %s' % fn)
#         with open('%s/%s' % (prevDriversDefined_dpath, fn), 'rb') as r_csvfile:
#             reader = csv.reader(r_csvfile)
#             headers = reader.next()
#             hid = {h: i for i, h in enumerate(headers)}
#             for row in reader:
#                 did1 = int(row[hid['did']])
#                 prevDrivers = row[hid['prevDrivers']].split('&')
#                 if len(prevDrivers) == 1 and prevDrivers[0] == '':
#                     continue
#                 if not driversRelations.has_key(did1):
#                     driversRelations[did1] = set()
#                 for did0 in map(int, prevDrivers):
#                     driversRelations[did1].add(did0)
#     save_pickle_file(driversRelations_fpaths[year], driversRelations)

if __name__ == '__main__':
    run()
