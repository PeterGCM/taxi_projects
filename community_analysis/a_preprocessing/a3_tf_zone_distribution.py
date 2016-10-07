import __init__
#
from community_analysis import ft_trips_dir, ft_trips_prefix
from community_analysis import tf_zone_counting_dir, ft_trips_prefix
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file, check_path_exist
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor


def run():
    check_dir_create(tf_zone_counting_dir)


if __name__ == '__main__':
    run()