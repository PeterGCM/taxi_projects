import __init__
#
from community_analysis import dw_aggreg_dir
from community_analysis import dw_filtered_dir, dw_filtered_prefix
#
from taxi_common.file_handling_functions import get_all_files, check_dir_create, load_pickle_file, \
    save_pickle_file, save_pkl_threading
from taxi_common.log_handling_functions import get_logger
#
import numpy as np

logger = get_logger('filtering')
percentiles = list(np.arange(99.9, 100, 0.01))


def run():
    check_dir_create(dw_filtered_dir)
    #
    for dw_aggreg_fn in get_all_files(dw_aggreg_dir, '', '.pkl'):
        logger.info('Start handling %s' % dw_aggreg_fn)
        dw_aggreg_fpath = '%s/%s' % (dw_aggreg_dir, dw_aggreg_fn)
        aggregated_dw_graph = load_pickle_file(dw_aggreg_fpath)
        logger.info('Finish loading %s' % dw_aggreg_fn)
        if len(dw_aggreg_fn.split('-')) == 4:
            handle_month3(dw_aggreg_fn, aggregated_dw_graph)
        else:
            handle_year(dw_aggreg_fn, aggregated_dw_graph)


def handle_month3(dw_month3_fn, month3_dw_graph):
    _, _, yyyy, duration = dw_month3_fn[:-len('.pkl')].split('-')
    month3_filtered_dw_graph = {th: {} for th in percentiles}
    weights = month3_dw_graph.values()
    threshold_values = [np.percentile(weights, pv) for pv in percentiles]
    logger.info('Start filtering %s' % dw_month3_fn)
    for k, v in month3_dw_graph.iteritems():
        for i, th in enumerate(threshold_values):
            if th < v:
                month3_filtered_dw_graph[percentiles[i]][k] = v
    #
    logger.info('Start pickling %s' % dw_month3_fn)
    for pv in percentiles:
        percentile_dir = '%s/percentile(%.2f)' % (dw_filtered_dir, pv)
        check_dir_create(percentile_dir)
        fpath = '%s/%s%s-%s-%s.pkl' % \
                            (percentile_dir, dw_filtered_prefix, 'percentile(%.2f)' % pv, yyyy, duration)
        save_pkl_threading(fpath, month3_filtered_dw_graph[pv])


def handle_year(dw_year_fn, year_dw_graph):
    _, _, yyyy = dw_year_fn[:-len('.pkl')].split('-')
    weights = year_dw_graph.values()
    threshold_values = [np.percentile(weights, pv) for pv in percentiles]
    for i, th in enumerate(threshold_values):
        pv = percentiles[i]
        year_filtered_dw_graph = {}
        logger.info('Start filtering %s , percentile(%.2f)' % (year_dw_graph, pv))
        for k, v in year_dw_graph.iteritems():
            if th < v:
                year_filtered_dw_graph[k] = v
        percentile_dir = '%s/percentile(%.2f)' % (dw_filtered_dir, pv)
        check_dir_create(percentile_dir)
        fpath = '%s/%s%s-%s.pkl' % \
                (percentile_dir, dw_filtered_prefix, 'percentile(%.2f)' % pv, yyyy)
        logger.info('Start pickling %s , percentile(%.2f)' % (year_dw_graph, pv))
        save_pickle_file(fpath, year_filtered_dw_graph)


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception filtering.txt', 'w') as f:
            f.write(format_exc())
        raise