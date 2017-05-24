import __init__
#
from community_analysis import FRI, SAT, SUN
from community_analysis import AM10, PM8
from community_analysis import taxi_home
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
from taxi_common.log_handling_functions import get_logger
from taxi_common.sg_grid_zone import get_sg_grid_xy_points
#
from bisect import bisect
import csv, datetime

logger = get_logger()

of_dpath = dpaths['driverTrip']
of_prefixs = prefixs['driverTrip']

try:
    check_dir_create(of_dpath)
except OSError:
    pass


def get_drivers_trip(yymm, drivers):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        yy, mm = yymm[:2], yymm[2:]
        trip_normal_fpath = '%s/20%s/%s/trips/trips-%s-normal.csv' % (taxi_home, yy, mm, yymm)
        trip_ext_fpath = '%s/20%s/%s/trips/trips-%s-normal-ext.csv' % (taxi_home, yy, mm, yymm)
        if not check_path_exist(trip_normal_fpath):
            logger.info('The file X exists; %s' % yymm)
            return None
        ofpath = None
        handling_day = 0
        x_points, y_points = get_sg_grid_xy_points()
        with open(trip_normal_fpath, 'rb') as tripFileN:
            tripReaderN = csv.reader(tripFileN)
            tripHeaderN = tripReaderN.next()
            hidN = {h: i for i, h in enumerate(tripHeaderN)}
            with open(trip_ext_fpath, 'rb') as tripFileE:
                tripReaderE = csv.reader(tripFileE)
                tripHeaderE = tripReaderE.next()
                hidE = {h: i for i, h in enumerate(tripHeaderE)}
                for rowN in tripReaderN:
                    rowE = tripReaderE.next()
                    didT = int(rowE[hidE['driver-id']])
                    if didT not in drivers:
                        continue
                    tripTime = eval(rowN[hidN['start-time']])
                    cur_dtT = datetime.datetime.fromtimestamp(tripTime)
                    if cur_dtT.weekday() in [FRI, SAT, SUN]:
                        continue
                    if cur_dtT.hour < AM10:
                        continue
                    if PM8 <= cur_dtT.hour:
                        continue
                    if handling_day != cur_dtT.day:
                        handling_day = cur_dtT.day
                        ofpath = '%s/%s%s%02d-%d.csv' % (of_dpath, of_prefixs, yymm, handling_day, '+'.join(map(str, drivers)))
                        with open(ofpath, 'wt') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            writer.writerow(['did',
                                             'hour', 'zi', 'zj',
                                             'time', 'day', 'month',
                                             'start-long', 'start-lat'])
                    s_long, s_lat = eval(rowN[hidN['start-long']]), eval(rowN[hidN['start-lat']])
                    zi, zj = bisect(x_points, s_long) - 1, bisect(y_points, s_lat) - 1
                    if zi < 0 or zj < 0:
                        continue
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow([didT,
                                         cur_dtT.hour, zi, zj,
                                         tripTime, cur_dtT.day, cur_dtT.month,
                                         s_long, s_lat])
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    get_drivers_trip('0901', 1)