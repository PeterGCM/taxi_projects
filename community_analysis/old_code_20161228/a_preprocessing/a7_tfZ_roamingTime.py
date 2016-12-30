import __init__
#
'''

'''
from community_analysis import taxi_home
from community_analysis import tfZ_roamingTime_dpath, tfZ_roamingTime_prefix
from community_analysis import FRI, SAT, SUN
from community_analysis import PM2, PM11
from community_analysis import FREE, POB
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, load_pickle_file, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
from bisect import bisect
import csv, datetime
#
logger = get_logger()


def run():
    check_dir_create(tfZ_roamingTime_dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in range(9, 11):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    from traceback import format_exc
    #
    try:
        logger.info('Handling %s' % yymm)
        tfZ_roamingTime_fpath = '%s/%s%s.pkl' % (tfZ_roamingTime_dpath, tfZ_roamingTime_prefix, yymm)
        if check_path_exist(tfZ_roamingTime_fpath):
            logger.info('Already processed; %s' % yymm)
            return None
        yy, mm = yymm[:2], yymm[-2:]
        yyyy = '20%s' % yy
        ss_drivers_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yyyy)
        if not check_path_exist(ss_drivers_fpath):
            logger.info('The file X exists; %s' % yyyy)
            return None
        #
        logger.info('loading ss drivers %s' % yymm)
        ss_drivers = load_pickle_file(ss_drivers_fpath)
        x_points, y_points = get_sg_grid_xy_points()
        #
        logger.info('Process roamingTime; %s' % yymm)
        log_fpath = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm)
        tfZ_roamingTime = {}
        with open(log_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            drivers = {}
            handling_day = 0
            for row in reader:
                did = int(row[hid['driver-id']])
                if did not in ss_drivers:
                    continue
                t = eval(row[hid['time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                if cur_dt.weekday() in [FRI, SAT, SUN]:
                    continue
                if cur_dt.hour < PM2:
                    continue
                if PM11 < cur_dt.hour:
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
                    logger.info('Processing %s %dth day' % (yymm, cur_dt.day))
                if not drivers.has_key(did):
                    drivers[did] = roaming_driver(did, tfZ_roamingTime, t, z, s)
                else:
                    drivers[did].update(t, z, s)
        save_pickle_file(tfZ_roamingTime_fpath, tfZ_roamingTime)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise

class roaming_driver(object):
    def __init__(self, did, tfZ_roamingTime, cl_time, cl_zone, cl_state):
        self.did = did
        self.tfZ_roamingTime = tfZ_roamingTime
        #
        # pl: previous log
        #
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state
        self.roaming_time = 0

    def update(self, cl_time, cl_zone, cl_state):
        if self.pl_state == FREE:
            if cl_state == FREE:
                self.roaming_time += cl_time - self.pl_time
            elif cl_state == POB:
                cl_dt = datetime.datetime.fromtimestamp(cl_time)
                zi, zj = cl_zone
                #
                k = (self.did, cl_dt.month, cl_dt.day, cl_dt.hour, zi, zj)
                self.tfZ_roamingTime[k] = self.roaming_time
                self.roaming_time = 0
            else:
                self.roaming_time = 0
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state

if __name__ == '__main__':
    run()