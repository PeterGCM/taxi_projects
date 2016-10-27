import __init__
#
from community_analysis import dw_graph_dir
from community_analysis import fdw_graph_dir, fdw_graph_prefix

#
from taxi_common.file_handling_functions import get_all_files, check_dir_create, load_pickle_file, \
    save_pickle_file, save_pkl_threading, check_path_exist
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import numpy as np
import csv
#
logger = get_logger('dw graph filtering')
PER_FROM, INTERVAL = 95.0, 1.0
percentiles = [pv for pv in np.arange(PER_FROM, 100, INTERVAL) if pv < 100]
fdw_graph_summary = '%s/%s(%.3f,%.3f).csv' % (fdw_graph_dir, 'fdw-graph-summary', PER_FROM, INTERVAL)


def run():
    check_dir_create(fdw_graph_dir)
    #
    if not check_path_exist(fdw_graph_summary):
        with open(fdw_graph_summary, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['period', 'numDrivers', 'numPickups', 'numLinks',
                                'weightAverage', 'weightSD',
                                'weightMedian', 'weightMin', 'weightMax']
            for per in percentiles:
                header.append('Percentile (%.3f)' % per)
            writer.writerow(header)
    #
    init_multiprocessor(3)
    count_num_jobs = 0
    for dw_graph_fn in get_all_files(dw_graph_dir, '', '.pkl'):
        put_task(handle_file, [dw_graph_fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def handle_file(dw_graph_fn):
    from traceback import format_exc
    #
    try:
        _, _, period = dw_graph_fn[:-len('.pkl')].split('-')
        logger.info('Start handling %s' % dw_graph_fn)
        dw_graph_fpath = '%s/%s' % (dw_graph_dir, dw_graph_fn)
        dw_graph = load_pickle_file(dw_graph_fpath)
        logger.info('Start filtering %s' % dw_graph_fn)
        num_drivers, num_pickups, num_links = 0, 0, 0
        graph = {}
        for did0, num_pickup, weighted_link in dw_graph:
            num_drivers += 1
            num_pickups += num_pickup
            for did1, weight in weighted_link.iteritems():
                k = (did0, did1)
                graph[k] = weight
        weights = graph.values()
        filtered_graph = {per: {} for per in percentiles}
        percentile_values = [np.percentile(weights, per) for per in percentiles]
        for k, v in graph.iteritems():
            for i, th in enumerate(percentile_values):
                if th < v:
                    filtered_graph[percentiles[i]][k] = v
        logger.info('Start pickling %s' % dw_graph_fn)
        for per in percentiles:
            percentile_dir = '%s/percentile(%.3f)' % (fdw_graph_dir, per)
            check_dir_create(percentile_dir)
            fpath = '%s/%s%s-%s.pkl' % \
                    (percentile_dir, fdw_graph_prefix, 'percentile(%.3f)' % per, period)
            save_pkl_threading(fpath, filtered_graph[per])
        #
        weights = np.asarray(weights)
        with open(fdw_graph_summary, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [period, num_drivers, num_pickups, len(weights),
                     weights.mean(), weights.std(),
                     np.median(weights), weights.min(), weights.max()]
            for pv in percentile_values:
                new_row.append('%.3f' % pv)
            writer.writerow(new_row)
    except Exception as _:
        with open('Exception filtering.txt', 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()