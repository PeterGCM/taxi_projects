import __init__
#
from community_analysis import fdwg_dir
from community_analysis import group_dir, group_prepix
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, check_dir_create, get_all_directories, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import louvain
import igraph as ig

logger = get_logger('partitioning')


def run():
    check_dir_create(group_dir)
    #
    init_multiprocessor(3)
    count_num_jobs = 0
    dw_per_dirs = get_all_directories(fdwg_dir)
    dw_per_dirs.reverse()
    for dw_per_dir_fn in dw_per_dirs:
        dw_per_dirpath = '%s/%s' % (fdwg_dir, dw_per_dir_fn)
        for dw_per_fn in get_all_files(dw_per_dirpath, '', '.pkl'):
            dw_per_fpath = '%s/%s' % (dw_per_dirpath, dw_per_fn)
            # process_file(dw_per_fpath, dw_per_fn)
            put_task(process_file, [dw_per_fpath, dw_per_fn])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(dw_per_fpath, dw_per_fn):
    from traceback import format_exc
    #
    try:
        _, _, percentile, period = dw_per_fn[:-len('.pkl')].split('-')
        group_per_dirpath = '%s/%s' % (group_dir, percentile)
        check_dir_create(group_per_dirpath)
        gp_targer_dirpath = '%s/%s' % (group_per_dirpath, period)
        if check_path_exist(gp_targer_dirpath):
            return None
        check_dir_create(gp_targer_dirpath)
        #
        logger.info('Start graph loading %s' % dw_per_fn)
        dw_graph = load_pickle_file(dw_per_fpath)
        num_edges = len(dw_graph)
        logger.info('igraph generation total number of edges %d' % num_edges)
        igid, did_igid = 0, {}
        igG = ig.Graph(directed=True)
        cur_percent = 0
        for i, ((did0, did1), w) in enumerate(dw_graph.iteritems()):
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
            group_fpath = '%s/%s%s-%s-G(%d).pkl' % (gp_targer_dirpath, group_prepix, percentile, period, i)
            sg.write_pickle(group_fpath)
    except Exception as _:
        with open('Exception partioning.txt', 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
