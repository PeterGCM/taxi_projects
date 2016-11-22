import __init__
#
'''

'''
#
from community_analysis import dwg_count_dir, dwg_count_prefix
from community_analysis import dwg_benefit_dir, dwg_benefit_prefix
from community_analysis import dwg_frequency_dir, dwg_frequency_prefix
from community_analysis import dwg_fb_dir, dwg_fb_prefix
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, save_pickle_file, check_dir_create
from taxi_common.log_handling_functions import get_logger
#
import time
#
logger = get_logger('aggregation')
FIVE_MINUTE = 5 * 60


def run():
    for dpath, fprefix in [(dwg_count_dir, dwg_count_prefix),
                            (dwg_benefit_dir, dwg_benefit_prefix),
                            (dwg_frequency_dir, dwg_frequency_prefix),
                            (dwg_fb_dir, dwg_fb_prefix)]:
        for y in range(9, 10):
            yyyy = '20%02d' % y
            logger.info('Handle %s (%s)' % yyyy, fprefix)
            year_aggregation_fpath = '%s/%s%s.pkl' % (dpath, fprefix, yyyy)
            if check_path_exist(year_aggregation_fpath):
                return None
            year_dwg = {}
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
                        if not year_dwg.has_key(k):
                            year_dwg[k] = 0.0
                        year_dwg[k] += weight
                #
            logger.info('Saving year_dw_graph %s' % yyyy)
            save_pickle_file(year_aggregation_fpath, {k: v for k, v in year_dwg.iteritems() if v > 0.0})


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        import sys
        with open('%s.txt' % (sys.argv[0]), 'w') as f:
            f.write(format_exc())
        raise
