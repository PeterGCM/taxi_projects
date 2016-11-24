import __init__
#
'''

'''
#
from community_analysis import group_dpath
from community_analysis import pickUp_dpath, pickUp_prepix
#
from taxi_common.file_handling_functions import check_dir_create, get_all_directories
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
logger = get_logger()


def run():
    check_dir_create(pickUp_dpath)
    #
    init_multiprocessor(6)
    count_num_jobs = 0
    for y in range(9, 10):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # yymm = '12%02d' % mm
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(period):
    pass
    # for group_wc_dname in get_all_directories(group_dpath):
    #     group_wc_dpath = '%s/%s' % (group_dpath, group_wc_dname)
    #     for group_wc_dname in get_all_directories(group_wc_dpath):

if __name__ == '__main__':
    run()
