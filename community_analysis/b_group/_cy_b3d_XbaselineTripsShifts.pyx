import __init__
#
'''

'''
#
from community_analysis import prevDriversDefined_dpath, prevDriversDefined_prefix
from community_analysis import dpaths, prefixs
# from community_analysis import shift_dpath, shift_prefix
from community_analysis import shiftProDur_dpath, shiftProDur_prefix
from community_analysis import X_PRESENCE, O_PRESENCE
from community_analysis import AM10, PM8
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
from taxi_common.log_handling_functions import get_logger
#
import csv
import pandas as pd
import igraph as ig
#
logger = get_logger()


def run():
    tm, year = 'baseline', '2009'

    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    check_dir_create(gt_dpath)
    gs_dpath = dpaths[tm, year, 'groupShifts']
    check_dir_create(gs_dpath)
    #
    gp_dpath = dpaths[tm, year, 'groupPartition']
    gp_prefix = prefixs[tm, year, 'groupPartition']
    gp_summary_fpath = '%s/%ssummary.csv' % (gp_dpath, gp_prefix)
    #
    gs_df = pd.read_csv(gp_summary_fpath)

    groupDrivers = set()
    for gn in gs_df['groupName'].values:
        igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn))
        for e in igG.es:
            did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
            groupDrivers.add(did0)
            groupDrivers.add(did1)
    process_file(tm, year, 'X', groupDrivers)


def process_file(tm, year, gn, groupDrivers):
    logger.info('handle the file; %s-%s-%s' % (tm, year, gn))
    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    gt_fpath = '%s/%s%s.csv' % (gt_dpath, gt_prefix, gn)
    #
    gs_dpath = dpaths[tm, year, 'groupShifts']
    gs_prefix = prefixs[tm, year, 'groupShifts']
    gs_fpath = '%s/%s%s.csv' % (gs_dpath, gs_prefix, gn)
    tm = 'spendingTime'
    with open(gt_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['time', 'year', 'month', 'day', 'hour',
                  'did', 'groupName',
                  'zi', 'zj', 'zizj',
                  tm, 'priorPresence',
                  'start-long', 'start-lat',
                  'distance', 'duration', 'fare']
        writer.writerow(header)
    with open(gs_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_headers = ['year', 'month', 'day', 'hour', 'did', 'pro-dur']
        writer.writerow(new_headers)
    yy = year[2:]
    tm = 'spendingTime'
    for fn in get_all_files(prevDriversDefined_dpath, 'Filtered-%s%s*' % (prevDriversDefined_prefix, yy)):
        fpath = '%s/%s' % (prevDriversDefined_dpath, fn)
        logger.info('handle the file %s; %s-%s-%s' % (fn, tm, year, gn))
        with open(fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            for row in reader:
                did1 = int(row[hid['did']])
                if did1 not in groupDrivers:
                    tm_value = row[hid[tm]]
                    t, month, day, hour = [row[hid[cn]] for cn in ['time', 'month', 'day', 'timeFrame']]
                    zi, zj = row[hid['zi']], row[hid['zj']]
                    zizj = '%s#%s' % (zi, zj)
                    _prevDrivers = row[hid['prevDrivers']].split('&')
                    priorPresence = X_PRESENCE
                    if len(_prevDrivers) == 1 and _prevDrivers[0] == '':
                        priorPresence = X_PRESENCE
                    else:
                        prevDrivers = map(int, _prevDrivers)
                        for did0 in groupDrivers.difference(set([did1])):
                            if did0 in prevDrivers:
                                priorPresence = O_PRESENCE
                                break
                    new_row = [t, year, month, day, hour,
                               did1, gn,
                               zi, zj, zizj,
                               tm_value, priorPresence]
                    for cn in ['start-long', 'start-lat', 'distance', 'duration', 'fare']:
                        new_row.append(row[hid[cn]])
                    with open(gt_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow(new_row)
    #
    yy = year[2:]
    for fn in get_all_files(shiftProDur_dpath, '%s%s*' % (shiftProDur_prefix, yy)):
        fpath = '%s/%s' % (shiftProDur_dpath, fn)
        with open(fpath, 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did1 = int(row[hid['did']])
                if did1 not in groupDrivers:
                    hour = int(row[hid['hour']])
                    if hour < AM10:
                        continue
                    if PM8 <= hour:
                        continue
                    with open(gs_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([row[hid['year']], row[hid['month']], row[hid['day']], hour,
                                     did1, row[hid['pro-dur']]])

if __name__ == '__main__':
    run()
