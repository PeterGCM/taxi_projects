import __init__
#
'''

'''
#
from community_analysis import fdwg_dir, fdw_graph_prefix
from community_analysis import group_dir, group_prepix
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, check_dir_create, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import louvain
import igraph as ig

logger = get_logger('___partitioning')


def run():
    check_dir_create(group_dir)
    #
    # init_multiprocessor(3)
    # count_num_jobs = 0
    for fdwg_fn in get_all_files(fdwg_dir, '', '.pkl'):
        process_file(fdwg_fn)
        # put_task(process_file, [dw_per_fpath, dw_per_fn])
    #     count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def process_file(fdwg_fn):
    from traceback import format_exc
    #
    try:
        logger.info('Start handling %s' % fdwg_fn)
        _, _, wc, period = fdwg_fn[:-len('.pkl')].split('-')
        group_wc_dpath = '%s/%s_%s' % (group_dir, wc, period)
        if check_path_exist(group_wc_dpath):
            logger.info('Already handled %s' % fdwg_fn)
            return None
        check_dir_create(group_wc_dpath)
        fdwg_fpath = '%s/%s' % (fdwg_dir, fdwg_fn)
        logger.info('Start graph loading %s' % fdwg_fpath)
        fdw_graph = load_pickle_file(fdwg_fpath)
        num_edges = len(fdw_graph)
        logger.info('igraph generation total number of edges %d' % num_edges)
        igid, did_igid = 0, {}
        igG = ig.Graph(directed=True)
        cur_percent = 0
        for i, ((did0, did1), w) in enumerate(fdw_graph):
            per = (i / float(num_edges))
            if per * 100 > cur_percent:
                cur_percent += 25
                logger.info('processed %.3f edges' % (i / float(num_edges)))
            if not did_igid.has_key(did0):
                igG.add_vertex(did0)
                did_igid[did0] = igid
                igid += 1
            if not did_igid.has_key(did1):
                igG.add_vertex(did1)
                did_igid[did1] = igid
                igid += 1
            igG.add_edge(did_igid[did0], did_igid[did1], weight=w)
        logger.info('Partitioning')
        part = louvain.find_partition(igG, method='Modularity', weight='weight')
        logger.info('Each group pickling')
        for i, sg in enumerate(part.subgraphs()):
            group_fpath = '%s/%s%s-%s-G(%d).pkl' % (group_wc_dpath, group_prepix, wc, period, i)
            sg.write_pickle(group_fpath)
    except Exception as _:
        import sys
        with open('___error_%s.txt' % (sys.argv[0]), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
