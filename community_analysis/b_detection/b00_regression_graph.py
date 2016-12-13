import __init__
#
'''

'''
#
from community_analysis import tfZ_RP_dpath, tfZ_RP_prepix
from community_analysis import RP_graph_dpath, RP_graph_prefix
from community_analysis import RP_group_dpath, RP_group_prefix
from community_analysis import RP_group_summary_fpath
from community_analysis import RP_group_drivers_fpath
from community_analysis import SIGINIFICANCE_LEVEL
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file, load_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import pandas as pd
import statsmodels.api as sm
import louvain
import igraph as ig
import csv, time

logger = get_logger()


def run():
    # check_dir_create(RP_graph_dpath)
    #
    # init_multiprocessor(2)
    # count_num_jobs = 0
    # for y in range(9, 10):
    #     yyyy = '20%02d' % y
    #     for tfZ_RP_fn in get_all_files(tfZ_RP_dpath, '%s%s*.csv' % (tfZ_RP_prepix, yyyy)):
    #         tfZ_RP_fpath = '%s/%s' % (tfZ_RP_dpath, tfZ_RP_fn)
    #         # process_file(tfZ_RP_fpath)
    #         put_task(process_file, [tfZ_RP_fpath])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)
    #
    check_dir_create(RP_group_dpath)
    if not check_path_exist(RP_group_summary_fpath):
        with open(RP_group_summary_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['period', 'groupName', 'numDrivers', 'tieStrength'])
    for y in range(9, 10):
        yyyy = '20%02d' % y
        merge_process(yyyy)



def merge_process(yyyy):
    RP_group_fpath = '%s/%s%s.pkl' % (RP_group_dpath, RP_group_prefix, yyyy)
    if check_path_exist(RP_group_fpath):
        return None
    RP_graph_year = {}
    for RP_graph_fn in get_all_files(RP_graph_dpath, '%s%s-*.pkl' % (RP_graph_prefix, yyyy)):
        RP_graph_fpath = '%s/%s' % (RP_graph_dpath, RP_graph_fn)
        RP_graph_batch = load_pickle_file(RP_graph_fpath)
        for k, v in RP_graph_batch.iteritems():
            RP_graph_year[k] = v
    #
    num_edges = len(RP_graph_year)
    logger.info('igraph generation total number of edges %d' % (num_edges))
    igid, did_igid = 0, {}
    igG = ig.Graph(directed=True)
    cur_percent = 0
    for i, ((did0, did1), w) in enumerate(RP_graph_year.iteritems()):
        per = (i / float(num_edges))
        if per * 100 > cur_percent:
            cur_percent += 1
            logger.info('processed %.2f edges' % (i / float(num_edges)))
        if not did_igid.has_key(did0):
            igG.add_vertex(did0)
            did_igid[did0] = igid
            igid += 1
        if not did_igid.has_key(did1):
            igG.add_vertex(did1)
            did_igid[did1] = igid
            igid += 1
        igG.add_edge(did_igid[did0], did_igid[did1], weight=abs(w))

    logger.info('Partitioning')
    part = louvain.find_partition(igG, method='Modularity', weight='weight')
    logger.info('Each group pickling and summary')
    group_drivers = {}
    for i, sg in enumerate(part.subgraphs()):
        gn = 'G(%d)' % i
        group_fpath = '%s/%s%s-%s.pkl' % (RP_group_dpath, RP_group_prefix, yyyy, gn)
        sg.write_pickle(group_fpath)
        #
        drivers = [v['name'] for v in sg.vs]
        weights = [e['weight'] for e in sg.es]
        with open(RP_group_summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([yyyy, gn, len(drivers), sum(weights) / float(len(drivers))])
        group_drivers[gn] = drivers
    save_pickle_file(RP_group_drivers_fpath, group_drivers)


def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    _, _, yyyy, reducerID = get_fn_only(fpath)[:-len('.pkl')].split('-')
    RP_graph_fpath = '%s/%s%s-%s.pkl' % (RP_graph_dpath, RP_graph_prefix, yyyy, reducerID)
    if check_path_exist(RP_graph_fpath):
        return None
    #
    logger.info('Start loading; %s-%s' % (yyyy, reducerID))
    df = pd.read_csv(fpath)
    RP_graph = {}
    num_drivers = len(set(df['did']))
    for i, did1 in enumerate(set(df['did'])):
        #
        logger.info('Doing regression %.2f' % (i / float(num_drivers)))
        did1_df = df[(df['did'] == did1)].copy(deep=True)
        data_multi_reg = did1_df.drop(['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did', '%d' % did1], axis=1)
        candi_dummies = []
        for i, vs in enumerate(zip(*data_multi_reg.values)):
            if data_multi_reg.columns[i] == 'roamingTime':
                continue
            if sum(vs) != 0:
                candi_dummies.append(data_multi_reg.columns[i])
        y = data_multi_reg['roamingTime']
        X = data_multi_reg[candi_dummies]
        X = sm.add_constant(X)
        res = sm.OLS(y, X, missing='drop').fit()
        if res.f_pvalue >= SIGINIFICANCE_LEVEL:
            continue
        significant_drivers = set()
        for _did0, pv in res.pvalues.iteritems():
            if _did0 == 'const':
                continue
            if pv < SIGINIFICANCE_LEVEL:
                significant_drivers.add(_did0)
        possitive_ef_drivers = set()
        for _did0, cof in res.params.iteritems():
            if _did0 == 'const':
                continue
            if cof > 0:
                possitive_ef_drivers.add(_did0)
        for _did0 in significant_drivers.difference(possitive_ef_drivers):
            RP_graph[int(_did0), did1] = res.params[_did0]
    logger.info('Start pickling; %s-%s' % (yyyy, reducerID))
    save_pickle_file(RP_graph_fpath, RP_graph)


if __name__ == '__main__':
    run()
