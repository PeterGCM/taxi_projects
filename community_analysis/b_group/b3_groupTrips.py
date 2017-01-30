import __init__
#
'''

'''
#
from community_analysis import prevDriversDefined_dpath, prevDriversDefined_prefix
from community_analysis import dpaths, prefixs
from community_analysis import X_PRESENCE, O_PRESENCE
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, load_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import pandas as pd
import igraph as ig
#
logger = get_logger()


def run():
    init_multiprocessor(11)
    count_num_jobs = 0
    for tm in ['spendingTime', 'roamingTime']:
        for year in ['2009', '2010', '2011', '2012']:
            gt_dpath = dpaths[tm, year, 'groupTrips']
            check_dir_create(gt_dpath)
            #
            gp_dpath = dpaths[tm, year, 'groupPartition']
            gp_prefix = prefixs[tm, year, 'groupPartition']
            gp_summary_fpath = '%s/%ssummary.csv' % (gp_dpath, gp_prefix)
            #
            gs_df = pd.read_csv(gp_summary_fpath)
            for gn in gs_df['groupName'].values:
                igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn))
                groupDrivers = set()
                for e in igG.es:
                    did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
                    groupDrivers.add(did0)
                    groupDrivers.add(did1)
                # process_file(tm, year, gn, groupDrivers)
                put_task(process_file, [tm, year, gn, groupDrivers])
                count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(tm, year, gn, groupDrivers):
    logger.info('handle the file; %s-%s-%s' % (tm, year, gn))
    gt_dpath = dpaths[tm, year, 'groupTrips']
    gt_prefix = prefixs[tm, year, 'groupTrips']
    gt_fpath = '%s/%s%s.csv' % (gt_dpath, gt_prefix, gn)
    yy = year[2:]
    with open(gt_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['time', 'year', 'month', 'day', 'hour'
                  'did', 'groupName'
                  'zi', 'zj', 'zizj',
                  tm, 'priorPresence',
                  'start-long', 'start-lat',
                  'distance', 'duration', 'fare']
        writer.writerow(header)
        for fn in get_all_files(prevDriversDefined_dpath, 'Filtered-%s%s*' % prevDriversDefined_prefix, yy):
            fpath = '%s/%s' % (prevDriversDefined_dpath, fn)
            logger.info('handle the file %s; %s-%s-%s' % (fn, tm, year, gn))
            with open(fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                header = reader.next()
                hid = {h: i for i, h in enumerate(header)}
                for row in reader:
                    did1 = int(row[hid['did']])
                    if did1 not in groupDrivers:
                        continue
                    tm_value = row[hid[tm]]
                    t, month, day, hour = [row[hid[cn]] for cn in ['time', 'month', 'day', 'timeFrame']]
                    zi, zj = row[hid['zi']], row[hid['zj']]
                    zizj = '%s#%s' % (zi, zj)
                    _prevDrivers = row[hid['prevDrivers']].split('&')
                    priorPresence = None
                    if len(_prevDrivers) == 1 and _prevDrivers[0] == '':
                        priorPresence = X_PRESENCE
                    else:
                        prevDrivers = map(int, _prevDrivers)
                        for did0 in groupDrivers.difference(set([did1])):
                            if did0 in prevDrivers:
                                priorPresence = O_PRESENCE
                                break
                        else:
                            priorPresence = X_PRESENCE
                    assert priorPresence != None
                    new_row = [t, year, month, day, hour,
                               did1, gn,
                               zi, zj, zizj,
                               tm_value, priorPresence]
                    for cn in ['start-long', 'start-lat', 'distance', 'duration', 'fare']:
                        new_row.append(row[hid[cn]])
                    writer.writerow(new_row)


if __name__ == '__main__':
    run()
