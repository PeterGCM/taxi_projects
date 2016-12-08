import __init__
#
'''

'''
#
from community_analysis import ss_trips_dpath, ss_trips_prefix
from community_analysis import pickUp_dpath, pickUp_prepix
#
from taxi_common.file_handling_functions import check_dir_create, get_all_directories, check_path_exist, load_pickle_file, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
logger = get_logger()


def run():
    check_dir_create(pickUp_dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in range(9, 10):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    from traceback import format_exc
    try:
        logger.info('handle period; %s' % yymm)
        ss_trips_fpath = '%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, yymm)
        if not check_path_exist(ss_trips_fpath):
            logger.info('The file X exists; %s' % ss_trips_fpath)
            return None
        logger.info('Process checking pickUp; %s' % yymm)
        pickUp = set()
        with open(ss_trips_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            handling_day = 0
            for row in reader:
                t = eval(row[hid['time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                day = cur_dt.day
                if handling_day != day:
                    handling_day = day
                    logger.info('handling; %s-%d' % (yymm, handling_day))
                did = int(row[hid['did']])
                tf = int(row[hid['timeFrame']])
                zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                k = (did, cur_dt.month, day, tf, zi, zj)
                pickUp.add(k)
        #
        logger.info('Pickling; %s' % yymm)
        pickUp_fpath = '%s/%s%s.pkl' % (pickUp_dpath, pickUp_prepix, yymm)
        save_pickle_file(pickUp_fpath, pickUp)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
