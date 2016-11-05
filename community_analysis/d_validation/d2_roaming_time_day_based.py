import __init__
#
from community_analysis import taxi_home
from community_analysis import roaming_time_dir, roaming_time_prefix
from community_analysis import roaming_time_ag_dir, roaming_time_ag_prefix
#
from taxi_common.file_handling_functions import check_path_exist, check_dir_create, load_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd

logger = get_logger('roaming_time_day')

def run():
    check_dir_create(roaming_time_ag_dir)
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
    from traceback import format_exc
    #
    try:
        roaming_time_fpath = '%s/%s%s.csv' % (roaming_time_dir, roaming_time_prefix, period)
        if not check_path_exist(roaming_time_fpath):
            logger.info('The file X exists; %s' % period)
            return None
        roaming_time_ag_fpath = '%s/%s%s.csv' % (roaming_time_ag_dir, roaming_time_ag_prefix, period)
        if check_path_exist(roaming_time_ag_fpath):
            logger.info('The file already handled; %s' % period)
            return None
        df = pd.read_csv(roaming_time_fpath)
        new_df = df.groupby(['did', 'timeFrame', 'zi', 'zj', 'day']).sum().loc[:, 'roamingTime'].reset_index()
        new_df.to_csv(roaming_time_ag_fpath)

    except Exception as _:
        with open('roaming time_%s.txt' % period, 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()