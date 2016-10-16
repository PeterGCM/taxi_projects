import __init__
#
from community_analysis import group_dir
from community_analysis import group_summary_fpath
#
from taxi_common.file_handling_functions import get_all_directories, get_all_files
#
from taxi_common.log_handling_functions import get_logger
#
import igraph as ig
import csv

logger = get_logger('summary')


def run():
    with open(group_summary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['percentile', 'period', 'groupName', 'numDrivers', 'tieStrength'])
    for group_per_dir in get_all_directories(group_dir):
        for period_dir in get_all_directories('%s/%s' % (group_dir, group_per_dir)):
            for com_fn in get_all_files('%s/%s/%s' % (group_dir, group_per_dir, period_dir), '', '.pkl'):
                com_dirpath = '%s/%s/%s' % (group_dir, group_per_dir, period_dir)
                fn_components = com_fn[:-len('.pkl')].split('-')
                logger.info('processing %s' % com_fn)
                if len(fn_components) == 5:
                    _, percentile, yyyy, months, group_name = fn_components
                    period = '%s(%s)' % (yyyy, months)
                else:
                    _, percentile, yyyy, group_name = fn_components
                    period = yyyy

                # print '%s/%s' % (com_dirpath, com_fn)
                igG = ig.Graph.Read_Pickle('%s/%s' % (com_dirpath, com_fn))
                drivers = [v['name'] for v in igG.vs]
                weights = [e['weight'] for e in igG.es]
                with open(group_summary_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([percentile, period, group_name, len(drivers), len(weights) / float(len(drivers))])


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception summary.txt', 'w') as f:
            f.write(format_exc())
        raise