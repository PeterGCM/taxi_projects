import __init__
#
'''

'''
from community_analysis import taxi_home
from community_analysis import group_dpath, group_prepix
from community_analysis import roamingTime_dpath, roamingTime_prepix
from community_analysis import FRI, SAT, SUN
from community_analysis import PM2, PM11
from community_analysis import FREE
#
from taxi_common.file_handling_functions import check_dir_create, get_all_directories, check_path_exist, load_pickle_file, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
from bisect import bisect
import csv, datetime
#
logger = get_logger()


def run():
    check_dir_create(roamingTime_dpath)
    #
    for wc in get_all_directories(group_dpath):
        roamingTime_wc_dpath = '%s/%s' % (roamingTime_dpath, wc)
        check_dir_create(roamingTime_wc_dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in range(10, 13):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(period):
    from traceback import format_exc
    #
    try:
        logger.info('Handling %s' % period)
        yy, mm = period[:2], period[-2:]
        log_fpath = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, period)
        if not check_path_exist(log_fpath):
            logger.info('The file X exists; %s' % period)
            return None
        #
        logger.info('load group drivers; %s' % period)
        yyyy = '20%s' % (period[:2])
        x_points, y_points = get_sg_grid_xy_points()
        for wc in get_all_directories(group_dpath):
            roamingTime_wc_dpath = '%s/%s' % (roamingTime_dpath, wc)
            roamingTime_fpath = '%s/%s%s-%s.pkl' % (roamingTime_wc_dpath, roamingTime_prepix, wc, period)
            if check_path_exist(roamingTime_fpath):
                logger.info('The file had already been processed; %s' % roamingTime_fpath)
                continue
            group_wc_dpath = '%s/%s' % (group_dpath, wc)
            group_drivers_fpath = '%s/%s%s-%s-drivers.pkl' % (group_wc_dpath, group_prepix, wc, yyyy)
            group_drivers = load_pickle_file(group_drivers_fpath)
            #
            logger.info('Process checking roamingTime; %s' % period)
            roamingTime = {}
            with open(log_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                drivers = {}
                handling_day = 0
                for row in reader:
                    t = eval(row[hid['time']])
                    cur_dt = datetime.datetime.fromtimestamp(t)
                    if cur_dt.weekday() in [FRI, SAT, SUN]:
                        continue
                    if cur_dt.hour < PM2:
                        continue
                    if PM11 < cur_dt.hour:
                        continue
                    did = int(row[hid['driver-id']])
                    for gn_drivers in group_drivers.itervalues():
                        if did in gn_drivers:
                            break
                    else:
                        continue
                    longitude, latitude = eval(row[hid['longitude']]), eval(row[hid['latitude']])
                    zi, zj = bisect(x_points, longitude) - 1, bisect(y_points, latitude) - 1
                    if zi < 0 or zj < 0:
                        continue
                    t, s = eval(row[hid['time']]), eval(row[hid['state']])
                    z = (zi, zj)
                    cur_dt = datetime.datetime.fromtimestamp(t)
                    if handling_day != cur_dt.day:
                        handling_day = cur_dt.day
                        logger.info('Processing %s %dth day' % (period, cur_dt.day))
                    if not drivers.has_key(did):
                        drivers[did] = roaming_driver(did, roamingTime, t, z, s)
                    else:
                        drivers[did].update(t, z, s)
            save_pickle_file(roamingTime_fpath, roamingTime)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], period), 'w') as f:
            f.write(format_exc())
        raise

class roaming_driver(object):
    def __init__(self, did, roamingTime, cl_time, cl_zone, cl_state):
        self.did = did
        self.roamingTime = roamingTime
        #
        # pl: previous log
        #
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state

    def update(self, cl_time, cl_zone, cl_state):
        if self.pl_state == FREE:
            pl_dt = datetime.datetime.fromtimestamp(self.pl_time)
            zi, zj = self.pl_zone
            roaming_time = cl_time - self.pl_time
            #
            k = (self.did, pl_dt.month, pl_dt.day, pl_dt.hour, zi, zj)
            if not self.roamingTime.has_key(k):
                self.roamingTime[k] = 0
            self.roamingTime[k] += roaming_time
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state

if __name__ == '__main__':
    run()