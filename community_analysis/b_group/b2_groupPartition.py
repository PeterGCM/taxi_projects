import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, load_pickle_file, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import louvain
import igraph as ig

logger = get_logger()


def run():
    # for tm in ['spendingTime', 'roamingTime']:

    init_multiprocessor(4)
    count_num_jobs = 0
    for tm in ['spendingTime']:
        for year in ['2009', '2010', '2011', '2012']:
            # process_file(tm, year)
            put_task(process_file, [tm, year])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(tm, year):
    ig_dpath = dpaths[tm, year, 'influenceGraph']
    ig_prefix = prefixs[tm, year, 'influenceGraph']
    gp_dpath = dpaths[tm, year, 'groupPartition']
    gp_prefix = prefixs[tm, year, 'groupPartition']
    #
    check_dir_create(gp_dpath)
    #
    gp_summary_fpath = '%s/%ssummary.csv' % (gp_dpath, gp_prefix)
    gp_original_fpath = '%s/%soriginal.pkl' % (gp_dpath, gp_prefix)
    gp_drivers_fpath = '%s/%sdrivers.pkl' % (gp_dpath, gp_prefix)
    #
    with open(gp_summary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['groupName', 'numDrivers', 'tieStrength', 'contribution'])
    #
    logger.info('Start handling SP_group_dpath')
    igid, did_igid = 0, {}
    igG = ig.Graph(directed=True)
    for fn in get_all_files(ig_dpath, '%s*' % ig_prefix):
        regression_graph = load_pickle_file('%s/%s' % (ig_dpath, fn))
        num_edges = len(regression_graph)
        cur_percent = 0
        for i, ((did0, did1), w) in enumerate(regression_graph.iteritems()):
            per = (i / float(num_edges))
            if per * 100 > cur_percent:
                cur_percent += 1
                logger.info('processed %.2f edges (%s)' % (i / float(num_edges), fn))
            if not did_igid.has_key(did0):
                igG.add_vertex(did0)
                did_igid[did0] = igid
                igid += 1
            if not did_igid.has_key(did1):
                igG.add_vertex(did1)
                did_igid[did1] = igid
                igid += 1
            igG.add_edge(did_igid[did0], did_igid[did1], weight=abs(w))
    orignal_graph = {}
    for e in igG.es:
        did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
        orignal_graph[did0, did1] = e['weight']
    save_pickle_file(gp_original_fpath, orignal_graph)
    #
    logger.info('Partitioning')
    part = louvain.find_partition(igG, method='Modularity', weight='weight')
    logger.info('Each group pickling and summary')
    gn_drivers = {}
    for i, sg in enumerate(part.subgraphs()):
        gn = 'G(%d)' % i
        group_fpath = '%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn)
        sg.write_pickle(group_fpath)
        #
        drivers = [v['name'] for v in sg.vs]
        weights = [e['weight'] for e in sg.es]
        tie_strength = sum(weights) / float(len(drivers))
        contribution = tie_strength / float(len(drivers))
        with open(gp_summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([gn, len(drivers), tie_strength, contribution])
        gn_drivers[gn] = drivers
    save_pickle_file(gp_drivers_fpath, gn_drivers)


if __name__ == '__main__':
    run()

