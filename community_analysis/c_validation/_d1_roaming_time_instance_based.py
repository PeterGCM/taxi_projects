import __init__
#
from community_analysis import taxi_home
from community_analysis import roaming_time_dir, roaming_time_prefix
from community_analysis import group_drivers_dir, group_drivers_prefix
from community_analysis import FREE
from community_analysis import CHOSEN_PERCENTILE
from community_analysis import FRI, SAT, SUN
from community_analysis import PM2, PM11
#
from taxi_common.file_handling_functions import check_path_exist, check_dir_create, load_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
from bisect import bisect
import csv, datetime

logger = get_logger('roaming_time')
percentile_dirname = 'percentile(%.3f)' % CHOSEN_PERCENTILE


def run():
    check_dir_create(roaming_time_dir)
    #
    init_multiprocessor(8)
    count_num_jobs = 0
    for y in range(9, 13):
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
        logger.info('Handling %s' % period)
        x_points, y_points = get_sg_grid_xy_points()

        group_drivers_fpath = '%s/%s/%s%s.pkl' % (group_drivers_dir, percentile_dirname, group_drivers_prefix, period)
        group_drivers = load_pickle_file(group_drivers_fpath)
        driver_set = set()
        for gn, members in group_drivers.iteritems():
            for did in members:
                driver_set.add(did)
        yy, mm = period[:2], period[-2:]
        log_fpath = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, period)
        if not check_path_exist(log_fpath):
            logger.info('The file X exists; %s' % period)
            return None
        roaming_time_fpath = '%s/%s%s.csv' % (roaming_time_dir, roaming_time_prefix, period)
        if check_path_exist(roaming_time_fpath):
            logger.info('The file already handled; %s' % period)
            return None
        with open(log_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            drivers = {}
            handling_day = 0
            for row in reader:
                did = row[hid['driver-id']]
                if did == '-1':
                    continue
                if eval(did) not in driver_set:
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
                    drivers[did] = driver(did, roaming_time_fpath,
                                          t, z, s)
                else:
                    drivers[did].update(t, z, s)
    except Exception as _:
        with open('roaming time_%s.txt' % period, 'w') as f:
            f.write(format_exc())
        raise


class driver(object):
    def __init__(self, did, roaming_time_fpath, cl_time, cl_zone, cl_state):
        self.did = did
        self.roaming_time_fpath = roaming_time_fpath
        #
        # pl: previous logging
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state
        #
        if not check_path_exist(self.roaming_time_fpath):
            with open(self.roaming_time_fpath, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(['did',
                                 'timeFrame', 'zi', 'zj',
                                 'roamingTime',
                                 'time', 'day', 'dayOfWeek'])

    def update(self, cl_time, cl_zone, cl_state):
        pl_dt = datetime.datetime.fromtimestamp(self.pl_time)
        count_true = 0
        if self.pl_state == FREE:
            count_true += 1
        if pl_dt.weekday() not in [FRI, SAT, SUN]:
            count_true += 1
        if PM2 < pl_dt.hour:
            count_true += 1
        if pl_dt.hour < PM11:
            count_true += 1
        #
        if count_true == 4:
            zi, zj = self.pl_zone
            roaming_time = cl_time - self.pl_time
            with open(self.roaming_time_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([self.did,
                                 pl_dt.hour, zi, zj,
                                 roaming_time,
                                 self.pl_time, pl_dt.day, pl_dt.weekday()])
        self.pl_time, self.pl_zone, self.pl_state = cl_time, cl_zone, cl_state


if __name__ == '__main__':
    run()