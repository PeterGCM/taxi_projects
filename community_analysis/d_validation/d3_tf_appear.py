import __init__
#
from community_analysis import com_trips_dir, com_trips_prefix
from community_analysis import tf_appear_dir, tf_appear_prefix
from community_analysis import CHOSEN_PERCENTILE
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime

logger = get_logger('df_appear')
percentile_dirname = 'percentile(%.3f)' % CHOSEN_PERCENTILE


def run():
    check_dir_create(tf_appear_dir)
    #
    init_multiprocessor(8)
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
        com_trips_fpath = '%s/%s/%s%s.csv' % (com_trips_dir, percentile_dirname, com_trips_prefix, period)
        if not check_path_exist(com_trips_fpath):
            logger.info('The file X exists; %s' % period)
            return None
        with open(com_trips_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:



                did = int(row[hid['did']])
                t = eval(row[hid['time']])
                day = int(row[hid['day']])
                zi, zj = int(row[hid['zi']]), int(row[hid['zj']])

    except Exception as _:
        with open('df_appear_%s.txt' % period, 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()