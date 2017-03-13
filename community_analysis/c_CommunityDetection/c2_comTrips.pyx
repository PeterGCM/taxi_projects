import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import X_PRESENCE, O_PRESENCE
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
from taxi_common.log_handling_functions import get_logger
#
import csv
import pandas as pd
import igraph as ig
#
logger = get_logger()
numWorkers = 7
#
year = '20%02d' % 9
depVar = 'roamingTime'
# depVar = 'interTravelTime'
#
#
if_dpath1 = dpaths['prevDrivers']
if_prefixs1 = prefixs['prevDrivers']
if_dpath2 = dpaths[depVar, 'graphPartition']
if_prefixs2 = prefixs[depVar, 'graphPartition']
of_dpath = dpaths[depVar, 'comTrips']
of_prefix = prefixs[depVar, 'comTrips']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(processorID):
    comSummary_fpath = '%s/%s%s-summary.csv' % (if_dpath2, if_prefixs2, year)
    #
    cs_df = pd.read_csv(comSummary_fpath)
    for i, cn in enumerate(cs_df['comName'].values):
        if i % numWorkers != processorID:
            continue
        igG = ig.Graph.Read_Pickle('%s/%s%s-%s.pkl' % (if_dpath2, if_prefixs2, year, cn))
        comDrivers = set()
        for e in igG.es:
            did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
            comDrivers.add(did0)
            comDrivers.add(did1)
        process_file(cn, comDrivers)


def process_file(comName, comDrivers):
    logger.info('handle the file; %s-%s' % (year, comName))
    ct_fpath = '%s/%s%s-%s.csv' % (of_dpath, of_prefix, year, comName)
    with open(ct_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['time', 'year', 'month', 'day', 'hour',
                  'did', 'groupName',
                  'zi', 'zj', 'zizj',
                  depVar, 'priorPresence',
                  'start-long', 'start-lat',
                  'distance', 'duration', 'fare']
        header += ['%d' % did0 for did0 in comDrivers]
        writer.writerow(header)
    yy = year[2:]
    for fn in get_all_files(if_dpath1, '%sFiltered-%s%s*' % (depVar, if_prefixs1, yy)):
        fpath = '%s/%s' % (if_dpath1, fn)
        logger.info('handle the file %s; %s-%s-%s' % (fn, depVar, year, comName))
        with open(fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            for row in reader:
                did1 = int(row[hid['did']])
                if did1 not in comDrivers:
                    continue
                tm_value = row[hid[depVar]]
                t, month, day, hour = [row[hid[colName]] for colName in ['time', 'month', 'day', 'hour']]
                zi, zj = row[hid['zi']], row[hid['zj']]
                zizj = '%s#%s' % (zi, zj)
                _prevDrivers = row[hid['prevDrivers']].split('&')
                priorPresence = X_PRESENCE
                if len(_prevDrivers) == 1 and _prevDrivers[0] == '':
                    priorPresence = X_PRESENCE
                else:
                    prevDrivers = map(int, _prevDrivers)
                    priorComDrivers = set()
                    for did0 in comDrivers.difference(set([did1])):
                        if did0 in prevDrivers:
                            priorComDrivers.add(did0)
                            priorPresence = O_PRESENCE
                new_row = [t, year, month, day, hour,
                           did1, comName,
                           zi, zj, zizj,
                           tm_value, priorPresence]
                for colName in ['start-long', 'start-lat', 'distance', 'duration', 'fare']:
                    new_row.append(row[hid[colName]])
                if priorPresence == X_PRESENCE:
                    new_row += [0 for _ in xrange(len(comDrivers))]
                else:
                    for did0 in comDrivers:
                        if did0 in priorComDrivers:
                            new_row += [1]
                        else:
                            new_row += [0]
                with open(ct_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)


if __name__ == '__main__':
    run(0)
