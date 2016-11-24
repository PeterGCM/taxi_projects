import __init__
#
'''

'''
#
from community_analysis import fdwg_dpath
from community_analysis import group_dpath, group_prepix
from community_analysis import group_summary_fpath
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, check_dir_create, get_all_files, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, time
import louvain
import igraph as ig

logger = get_logger()
LOCK = False


def run():
    check_dir_create(group_dpath)
    if not check_path_exist(group_summary_fpath):
        with open(group_summary_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['weightCalculation', 'period', 'groupName', 'numDrivers', 'tieStrength'])
    #
    init_multiprocessor(4)
    count_num_jobs = 0
    for fdwg_fn in get_all_files(fdwg_dpath, '', '.pkl'):
        # process_file(fdwg_fn)
        put_task(process_file, [fdwg_fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(fdwg_fn):
    from traceback import format_exc
    #
    try:
        logger.info('Start handling %s' % fdwg_fn)
        _, _, wc, period = fdwg_fn[:-len('.pkl')].split('-')
        group_wc_dpath = '%s/%s' % (group_dpath, wc)
        group_drivers_fpath = '%s/%s%s-%s-drivers.pkl' % (group_wc_dpath, group_prepix, wc, period)
        if check_path_exist(group_drivers_fpath):
            logger.info('Already handled %s' % group_drivers_fpath)
            return None
        check_dir_create(group_wc_dpath)
        fdwg_fpath = '%s/%s' % (fdwg_dpath, fdwg_fn)
        logger.info('Start graph loading %s' % fdwg_fpath)
        fdw_graph = load_pickle_file(fdwg_fpath)
        num_edges = len(fdw_graph)
        logger.info('igraph generation total number of edges %d (%s)' % (num_edges, wc))
        igid, did_igid = 0, {}
        igG = ig.Graph(directed=True)
        cur_percent = 0
        for i, ((did0, did1), w) in enumerate(fdw_graph):
            per = (i / float(num_edges))
            if per * 100 > cur_percent:
                cur_percent += 1
                logger.info('processed %.2f edges (%s)' % (i / float(num_edges), wc))
            if not did_igid.has_key(did0):
                igG.add_vertex(did0)
                did_igid[did0] = igid
                igid += 1
            if not did_igid.has_key(did1):
                igG.add_vertex(did1)
                did_igid[did1] = igid
                igid += 1
            igG.add_edge(did_igid[did0], did_igid[did1], weight=w)
        #
        logger.info('Partitioning')
        part = louvain.find_partition(igG, method='Modularity', weight='weight')
        #
        logger.info('Each group pickling and summary')
        group_drivers = {}
        for i, sg in enumerate(part.subgraphs()):
            gn = 'G(%d)' % i
            group_fpath = '%s/%s%s-%s-%s.pkl' % (group_wc_dpath, group_prepix, wc, period, gn)
            sg.write_pickle(group_fpath)
            #
            drivers = [v['name'] for v in sg.vs]
            weights = [e['weight'] for e in sg.es]
            while True:
                global LOCK
                if not LOCK:
                    LOCK = True
                    with open(group_summary_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([wc, period, gn, len(drivers), sum(weights) / float(len(drivers))])
                    LOCK = False
                    break
                else:
                    time.sleep(1)
            group_drivers[gn] = drivers
        save_pickle_file(group_drivers_fpath, group_drivers)
    except Exception as _:
        import sys
        with open('___error_%s.txt' % (sys.argv[0]), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
