import __init__
#
'''

'''
#
from community_analysis import SP_group_drivers_fpath
from community_analysis import ss_trips_dpath, ss_trips_prefix
from community_analysis import SP_groupDefinedTrip_dpath, SP_groupDefinedTrip_prefix
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, load_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
logger = get_logger()


def run():
    check_dir_create(SP_groupDefinedTrip_dpath)
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


def process_month(yymm):
    logger.info('handle the file; %s' % yymm)
    group_drivers = load_pickle_file(SP_group_drivers_fpath)

    did_gn = {}
    for gn, members in group_drivers.iteritems():
        for did in members:
            did_gn[did] = gn
    groupDefinedTrip_fpath = '%s/%s%s.csv' % (SP_groupDefinedTrip_dpath, SP_groupDefinedTrip_prefix, yymm)
    if check_path_exist(groupDefinedTrip_fpath):
        logger.info('The processed; %s' % yymm)
        return None
    with open(groupDefinedTrip_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['did',
                         'timeFrame', 'zi', 'zj',
                         'time', 'day', 'month',
                         'start-long', 'start-lat',
                         'distance', 'duration', 'fare',
                         'groupName'])
        handling_day = 0
        with open('%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did = int(row[hid['did']])
                t = eval(row[hid['time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                if handling_day != cur_dt.day:
                    logger.info('Processing %s %dth day (month %d)' % (yymm, cur_dt.day, cur_dt.month))
                    handling_day = cur_dt.day
                if not did_gn.has_key(did):
                    continue
                gn = did_gn[did]
                new_row = [row[hid[cn]] for cn in ['did',
                                                    'timeFrame', 'zi', 'zj',
                                                    'time', 'day', 'month',
                                                    'start-long', 'start-lat',
                                                    'distance', 'duration', 'fare']]
                new_row += [gn]
                writer.writerow(new_row)

if __name__ == '__main__':
    run()
