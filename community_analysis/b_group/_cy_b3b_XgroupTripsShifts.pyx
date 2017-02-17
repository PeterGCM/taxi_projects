import __init__
#
'''

'''
#
from community_analysis import prevDriversDefined_dpath, prevDriversDefined_prefix
from community_analysis import shift_dpath, shift_prefix
from community_analysis import dpaths, prefixs
from community_analysis import X_PRESENCE, O_PRESENCE
from community_analysis import AM10, PM8
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import csv, gzip
import pandas as pd
import igraph as ig
#
logger = get_logger()


def run():
    tm, year = 'spendingTime', '2009'
    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    check_dir_create(gt_dpath)
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
    # gt_dpath = dpaths[tm, year, 'groupTrips']
    # gt_prefix = prefixs[tm, year, 'groupTrips']
    # gt_fpath = '%s/%s%s.csv' % (gt_dpath, gt_prefix, gn)
    #
    gs_dpath = dpaths[tm, year, 'groupShifts']
    gs_prefix = prefixs[tm, year, 'groupShifts']
    gs_fpath = '%s/%s%s.csv' % (gs_dpath, gs_prefix, gn)
    # xgt_fpath = '%s/%s%s.csv' % (gt_dpath, gt_prefix, 'X')
    # assert xgt_fpath == gt_fpath, (gt_fpath)
    # with open(xgt_fpath, 'wt') as w_csvfile:
    #     writer = csv.writer(w_csvfile, lineterminator='\n')
    #     header = ['time', 'year', 'month', 'day', 'hour',
    #               'did', 'groupName',
    #               'zi', 'zj', 'zizj',
    #               tm, 'priorPresence',
    #               'start-long', 'start-lat',
    #               'distance', 'duration', 'fare']
    #     writer.writerow(header)
    # yy = year[2:]
    # for fn in get_all_files(prevDriversDefined_dpath, 'Filtered-%s%s*' % (prevDriversDefined_prefix, yy)):
    #     fpath = '%s/%s' % (prevDriversDefined_dpath, fn)
    #     logger.info('handle the file %s; %s-%s-%s' % (fn, tm, year, gn))
    #     with open(fpath, 'rb') as r_csvfile:
    #         reader = csv.reader(r_csvfile)
    #         header = reader.next()
    #         hid = {h: i for i, h in enumerate(header)}
    #         for row in reader:
    #             did1 = int(row[hid['did']])
    #             if did1 not in groupDrivers:
    #                 with open(xgt_fpath, 'a') as w_csvfile:
    #                     writer = csv.writer(w_csvfile, lineterminator='\n')
    #                     new_row = [row[hid['time']], year]
    #                     new_row += [row[hid[cn]] for cn in ['month', 'day', 'timeFrame']]
    #                     new_row += [did1, 'X']
    #                     zi, zj = row[hid['zi']], row[hid['zj']]
    #                     zizj = '%s#%s' % (zi, zj)
    #                     new_row += [zi, zj, zizj]
    #                     new_row += [row[hid[tm]], 'X']
    #                     for cn in ['start-long', 'start-lat', 'distance', 'duration', 'fare']:
    #                         new_row.append(row[hid[cn]])
    #                     writer.writerow(new_row)
    yy = year[2:]
    productive_state = ['dur%d' % x for x in [0, 3, 4, 5, 6, 7, 8, 9, 10]]
    for fn in get_all_files(shift_dpath, '%s%s*' % (shift_prefix, yy)):
        _, _, _, yymm = fn[:-len('.csv.gz')].split('-')
        if yymm == '1010':
            continue
        fpath = '%s/%s' % (shift_dpath, fn)
        with gzip.open(fpath, 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did1 = int(row[hid['driver-id']])
                if did1 not in groupDrivers:
                    hour = int(row[hid['hour']])
                    if hour < AM10:
                        continue
                    if PM8 <= hour:
                        continue
                    productive_duration = sum(int(row[hid[dur]]) for dur in productive_state)
                    with open(gs_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([row[hid['year']], row[hid['month']], row[hid['day']], hour,
                                         did1, productive_duration])


if __name__ == '__main__':
    run()
