import __init__
#
'''

'''
#
from community_analysis import dwg_count_dpath, dwg_count_prefix
from community_analysis import dwg_benefit_dpath, dwg_benefit_prefix
from community_analysis import dwg_frequency_dpath, dwg_frequency_prefix
from community_analysis import dwg_fb_dpath, dwg_fb_prefix
from community_analysis import dwg_summary_fpath
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, save_pickle_file, check_dir_create
from taxi_common.log_handling_functions import get_logger
#
import numpy as np
import csv, time
#
logger = get_logger()
FIVE_MINUTE = 5 * 60


def run():
    if not check_path_exist(dwg_summary_fpath):
        with open(dwg_summary_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['period', 'weightCalculation',
                      'numDrivers', 'numLinks',
                      'weightAverage', 'weightSD',
                      'weightMedian', 'weightMin', 'weightMax']
            writer.writerow(header)
    for dpath, fprefix in [
                            # (dwg_count_dpath, dwg_count_prefix),
                            (dwg_benefit_dpath, dwg_benefit_prefix),
                            # (dwg_frequency_dpath, dwg_frequency_prefix),
                            # (dwg_fb_dpath, dwg_fb_prefix)
                           ]:
        for y in range(9, 10):
            yyyy = '20%02d' % y
            logger.info('Handle %s (%s)' % (yyyy, fprefix))
            year_aggregation_fpath = '%s/%s%s.pkl' % (dpath, fprefix, yyyy)
            if check_path_exist(year_aggregation_fpath):
                logger.info('Already handled %s (%s)' % (yyyy, fprefix))
                return None
            year_dwg = {}
            drivers = set()
            for m in range(1, 13):
                yymm = '%02d%02d' % (y, m)
                logger.info('Loading %s' % yymm)
                month_dwg_fpath = '%s/%s%s.pkl' % (dpath, fprefix, yymm)
                if not check_path_exist(month_dwg_fpath):
                    continue
                #
                month_dwg = load_pickle_file(month_dwg_fpath)
                num_drivers = len(month_dwg)
                old_time = time.time()
                for i, (did0, num_pickup, weighted_link) in enumerate(month_dwg):
                    cur_time = time.time()
                    if cur_time - old_time > FIVE_MINUTE:
                        logger.info('processed %s %.3f' % (yymm, i / float(num_drivers)))
                        old_time = cur_time
                    for did1, weight in weighted_link.iteritems():
                        k = (did0, did1)
                        drivers.add(did0); drivers.add(did1)
                        if not year_dwg.has_key(k):
                            year_dwg[k] = 0.0
                        year_dwg[k] += weight
            #
            logger.info('Saving year_dw_graph %s' % yyyy)
            save_pickle_file(year_aggregation_fpath, year_dwg)
            weights = np.asarray(year_dwg.values())
            with open(dwg_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([yyyy, fprefix.split('-')[2],
                                 len(drivers), len(year_dwg),
                                 weights.mean(), weights.std(),
                                 np.median(weights), weights.min(), weights.max()])

if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        import sys
        with open('___error_%s.txt' % (sys.argv[0]), 'w') as f:
            f.write(format_exc())
        raise
