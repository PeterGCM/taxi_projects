import __init__
#
'''

'''
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

logger = get_logger()


def run():
    with open(group_summary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['weightCalculation', 'period', 'groupName', 'numDrivers', 'tieStrength'])
    for group_wc_dn in get_all_directories(group_dir):
        group_wc_dpath = '%s/%s' % (group_dir, group_wc_dn)
        for group_fn in get_all_files(group_wc_dpath, '', '.pkl'):
            _, wc, period, group_name = group_fn[:-len('.pkl')].split('-')
            group_fpath = '%s/%s' % (group_wc_dpath, group_fn)
            logger.info('processing %s' % group_fn)
            igG = ig.Graph.Read_Pickle(group_fpath)
            drivers = [v['name'] for v in igG.vs]
            weights = [e['weight'] for e in igG.es]
            with open(group_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([wc, period, group_name, len(drivers), sum(weights) / float(len(drivers))])


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception summary.txt', 'w') as f:
            f.write(format_exc())
        raise