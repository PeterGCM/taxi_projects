import __init__
#
'''

'''
#
from community_analysis import prevDriversDefined_dpath, prevDriversDefined_prefix
from community_analysis import driversRelations2009_fpath
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files

def run():
    check_dir_create(driversRelations_dpath)
    #





    init_multiprocessor(6)
    count_num_jobs = 0
    for y in range(9, 10):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_month(yymm)
            put_task(process_month, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)