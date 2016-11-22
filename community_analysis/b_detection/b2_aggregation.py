import __init__
#
from community_analysis import dwg_dir, dwg_prefix
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, save_pickle_file, check_dir_create
from taxi_common.log_handling_functions import get_logger
#
import time
#
logger = get_logger('aggregation')
FIVE_MINUTE = 5 * 60


def run():
    check_dir_create(dwg_dir)
    #
    for y in range(9, 13):
        yyyy = '20%02d' % y
        logger.info('Handle %s' % yyyy)
        year_aggregation_fpath = '%s/%s%s.pkl' % (dwg_dir, dwg_prefix, yyyy)
        if check_path_exist(year_aggregation_fpath):
            return None
        year_dw_graph = {}
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            logger.info('Loading %s' % yymm)
            month_dw_graph_fpath = '%s/%s%s.pkl' % (dwg_dir, dwg_prefix, yymm)
            if not check_path_exist(month_dw_graph_fpath):
                continue
            #
            month_dw_graph = load_pickle_file(month_dw_graph_fpath)
            num_drivers = len(month_dw_graph)
            old_time = time.time()
            for i, (did0, num_pickup, weighted_link) in enumerate(month_dw_graph):
                cur_time = time.time()
                if cur_time - old_time > FIVE_MINUTE:
                    logger.info('processed %s %.3f' % (yymm, i / float(num_drivers)))
                    old_time = cur_time
                for did1, weight in weighted_link.iteritems():
                    k = (did0, did1)
                    if not year_dw_graph.has_key(k):
                        year_dw_graph[k] = 0.0
                    year_dw_graph[k] += weight
            #
        logger.info('Saving year_dw_graph0 %s' % yyyy)
        save_pickle_file(year_aggregation_fpath, {k: v for k, v in year_dw_graph.iteritems() if v > 0.0})


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception aggregation.txt', 'w') as f:
            f.write(format_exc())
        raise
