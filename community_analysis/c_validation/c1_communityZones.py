import __init__
#
'''

'''
#
from community_analysis import SP_group_dpath, SP_group_prefix
from community_analysis import RP_group_dpath, RP_group_prefix
from community_analysis import SP_comZones_dpath, SP_comZones_prefix
from community_analysis import RP_comZones_dpath, RP_comZones_prefix
from community_analysis import SP_group_summary_fpath
from community_analysis import RP_group_summary_fpath
from community_analysis import prevDriversDefined_dpath, prevDriversDefined_prefix
from community_analysis import X_PRESENCE, O_PRESENCE
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
import igraph as ig
import csv

logger = get_logger()


def run():
    for dpath in [SP_comZones_dpath, RP_comZones_dpath]:
        check_dir_create(dpath)
    #
    init_multiprocessor(7)
    count_num_jobs = 0
    #
    for timeMeasure, zDpath, zPrefix, gDpath, gPrefix, gsFath in \
                    [('spendingTime', SP_comZones_dpath, SP_comZones_prefix, SP_group_dpath, SP_group_prefix, SP_group_summary_fpath),
                     ('roamingTime', RP_comZones_dpath, RP_comZones_prefix, RP_group_dpath, RP_group_prefix, RP_group_summary_fpath)]:
        group_df = pd.read_csv(gsFath)
        group_df = group_df.sort_values(by='contribution', ascending=False)
        # for gn in group_df.head(10)['groupName'].values:
        for gn in group_df['groupName'].values:
            igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (gDpath, gPrefix, gn))
            group_drivers = set()
            for e in igG.es:
                did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
                group_drivers.add(did0)
                group_drivers.add(did1)
            # process_file(timeMeasure, gn, group_drivers, zDpath, zPrefix)
            put_task(process_file, [timeMeasure, gn, group_drivers, zDpath, zPrefix])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(timeMeasure, gn, group_drivers, zDpath, zPrefix):
    logger.info('handle %s%s' % (zPrefix, gn))
    #
    comZones_fpath = '%s/%s%s.csv' % (zDpath, zPrefix, gn)
    with open(comZones_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['did', 'zizj', 'timeMeasure','priorPresence']
        writer.writerow(header)
        for fn in get_all_files(prevDriversDefined_dpath, 'Filtered-%s*' % prevDriversDefined_prefix):
            fpath = '%s/%s' % (prevDriversDefined_dpath, fn)
            logger.info('handle %s; %s%s' % (fn, zPrefix, gn))
            with open(fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                header = reader.next()
                hid = {h: i for i, h in enumerate(header)}
                for row in reader:
                    did1 = int(row[hid['did']])
                    if did1 not in group_drivers:
                        continue
                    zi, zj = row[hid['zi']], row[hid['zj']]
                    zizj = '%s#%s' % (zi, zj)
                    _prevDrivers = row[hid['prevDrivers']].split('&')
                    if len(_prevDrivers) == 1 and _prevDrivers[0] == '':
                        new_row = [did1, zizj, row[hid[timeMeasure]], X_PRESENCE]
                    else:
                        prevDrivers = map(int, _prevDrivers)
                        for did0 in group_drivers.difference(set([did1])):
                            if did0 in prevDrivers:
                                new_row = [did1, zizj, row[hid[timeMeasure]], O_PRESENCE]
                                break
                        else:
                            new_row = [did1, zizj, row[hid[timeMeasure]], X_PRESENCE]
                    writer.writerow(new_row)


if __name__ == '__main__':
    run()
