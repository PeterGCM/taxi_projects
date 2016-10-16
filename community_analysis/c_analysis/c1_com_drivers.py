import __init__
#
from community_analysis import group_dir
from community_analysis import com_drivers_dir, com_drivers_prefix
from community_analysis import CHOSEN_PERCENTILE, MIN_NUM_DRIVERS
#
from taxi_common.file_handling_functions import check_dir_create, get_all_directories, get_all_files, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import igraph as ig

logger = get_logger('com_drivers')


def run():
    check_dir_create(com_drivers_dir)
    #
    percentile_dirname = 'percentile(%.3f)' % CHOSEN_PERCENTILE
    check_dir_create('%s/%s' % (com_drivers_dir, percentile_dirname))
    #
    percentile_dirpath = '%s/%s' % (group_dir, percentile_dirname)
    for dirname in get_all_directories(percentile_dirpath):
        if len(dirname) > len('yyyy'):
            continue
        year_dirpath = '%s/%s' % (percentile_dirpath, dirname)
        year_com_fpath = '%s/%s/%s%s.pkl' % (com_drivers_dir, percentile_dirname, com_drivers_prefix, dirname)
        year_communities = {}
        for group_fn in get_all_files(year_dirpath, '', '.pkl'):
            _, _, yyyy, g_name = group_fn[:-len('.pkl')].split('-')
            igG = ig.Graph.Read_Pickle('%s/%s' % (year_dirpath, group_fn))
            drivers = [v['name'] for v in igG.vs]
            if len(drivers) < MIN_NUM_DRIVERS:
                continue
            year_communities[g_name] = drivers
        save_pickle_file(year_com_fpath, year_communities)











if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception com_drivers.txt', 'w') as f:
            f.write(format_exc())
        raise
