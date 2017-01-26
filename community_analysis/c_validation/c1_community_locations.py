import __init__
#
'''

'''
#
from community_analysis import SP_group_dpath, SP_group_prefix
from community_analysis import RP_group_dpath, RP_group_prefix
from community_analysis import SP_zone_dpath, SP_zone_prefix
from community_analysis import RP_zone_dpath, RP_zone_prefix
from community_analysis import SP_group_summary_fpath
from community_analysis import RP_group_summary_fpath
from community_analysis import driversRelations2009_fpath
from community_analysis import tfZ_TP_dpath, tfZ_TP_prefix
#
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
import igraph as ig
import csv

logger = get_logger()


def run():
    check_dir_create(SP_zone_dpath)
    # check_dir_create(RP_zone_dpath)
    #
    driversRelations = load_pickle_file(driversRelations2009_fpath)
    #
    numWorker = 6
    numReducers = numWorker * 10
    whole_drivers = driversRelations.keys()
    did_reducerID = {}
    for i, did in enumerate(whole_drivers):
        did_reducerID[did] = i % numReducers
    #
    # init_multiprocessor(numWorker)
    # count_num_jobs = 0

    group_df = pd.read_csv(SP_group_summary_fpath)
    # group_df = pd.read_csv(RP_group_summary_fpath)

    group_df = group_df.sort_values(by='contribution', ascending=False)
    for gn in group_df.head(10)['groupName'].values:
        process_file(gn, did_reducerID)
    #     put_task(process_file, [gn, did_reducerID])
    #     count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def process_file(gn, did_reducerID):
    logger.info('handle %s' % gn)
    igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (SP_group_dpath, SP_group_prefix, gn))
    # igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (RP_group_dpath, RP_group_prefix, gn))
    for e in igG.es:
        did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
        #
        tfZ_TP_fpath = '%s/%s%s-%d.csv' % (tfZ_TP_dpath, tfZ_TP_prefix, '2009', did_reducerID[did1])
        TP_df = pd.read_csv(tfZ_TP_fpath)
        zizj_t = {}
        for zi, zj, t in TP_df[(TP_df['did'] == did1) & (TP_df['%d' % did0])].loc[:, ['zi', 'zj', 'spendingTime']].values:
        # for zi, zj, t in TP_df[(TP_df['did'] == did1) & (TP_df['%d' % did0])].loc[:, ['zi', 'zj', 'roamingTime']].values:
            k = (zi, zj)
            if not zizj_t.has_key(k):
                zizj_t[k] = []
            zizj_t[k].append(t)
        with open('%s/%s%s-%d-%d.csv' % (SP_zone_dpath, SP_zone_prefix, gn, did0, did1), 'wt') as w_csvfile:
        # with open('%s/%s%s-%d-%d.csv' % (RP_zone_dpath, RP_zone_prefix, gn, did0, did1), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['spendingTime']
            # header = ['roamingTime']
            for zi, zj in zizj_t.iterkeys():
                header.append('%d#%d' % (zi, zj))
            writer.writerow(header)
            for (zi0, zj0), ts in zizj_t.iteritems():
                for t in ts:
                    new_row = [t]
                    for zi1, zj1 in zizj_t.iterkeys():
                        if (zi0, zj0) == (zi1, zj1):
                            new_row.append(1)
                        else:
                            new_row.append(0)
                    writer.writerow(new_row)


if __name__ == '__main__':
    run()
