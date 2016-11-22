import __init__
#
from community_analysis import dwg_count_dir, dwg_count_prefix
from community_analysis import dwg_benefit_dir, dwg_benefit_prefix
from community_analysis import dwg_frequency_dir, dwg_frequency_prefix
from community_analysis import dwg_fb_dir, dwg_fb_prefix
from community_analysis import fdwg_dir, fdw_graph_prefix
from community_analysis import TOP5PERCENT
#
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file, \
                                                save_pickle_file, check_path_exist
from taxi_common.log_handling_functions import get_logger
#
logger = get_logger('dw graph filtering')


def run():
    check_dir_create(fdwg_dir)
    #
    for y in range(9, 10):
        yyyy = '20%02d' % y
        process_file(yyyy)


def process_file(period):
    from traceback import format_exc
    #
    try:
        logger.info('Handle %s' % (period))
        for dpath, fprefix in [(dwg_count_dir, dwg_count_prefix),
                               (dwg_benefit_dir, dwg_benefit_prefix),
                               (dwg_frequency_dir, dwg_frequency_prefix),
                               # (dwg_fb_dir, dwg_fb_prefix)
                               ]:
            fdw_graph_fpath = '%s/%s%s-%s.pkl' % (fdwg_dir, fdw_graph_prefix, fprefix.split('-')[2], period)
            if check_path_exist(fdw_graph_fpath):
                logger.info('Already exist %s' % (fdw_graph_fpath))
                continue
            dwg_fpath = '%s/%s%s' % (dpath, fprefix, period)
            if not check_path_exist(dwg_fpath):
                logger.info('Not exist %s' % (dwg_fpath))
                continue
            dw_graph = load_pickle_file(dwg_fpath)
            save_pickle_file(fdw_graph_fpath,
                             sorted([(k, v) for k, v in dw_graph.iteritems()], key=lambda x: x[1], reverse=True)[
                             :int(len(dw_graph) * TOP5PERCENT)])
    except Exception as _:
        import sys
        with open('___error_%s.txt' % (sys.argv[0]), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()