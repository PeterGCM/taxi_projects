import __init__
#
from community_analysis import dpaths, prefixs
import GPS_xyCoords_converter as GPS_xyDrawing
#
from taxi_common.file_handling_functions import check_path_exist, get_all_files, save_pickle_file, load_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime
#

logger = get_logger()

if_dpath = dpaths['driverLog']
if_prefix = prefixs['driverLog']


def run():
    drivers_dates = {}
    for fn in get_all_files(if_dpath, '%s*.csv' % if_prefix):
        _, _date, _did = fn[:-len('.csv')].split('-')
        year = 2000 + int(_date[:2])
        month, day = map(int, [_date[2:4], _date[4:6]])
        dt = datetime.datetime(year, month, day)
        k = int(_did)
        if not drivers_dates.has_key(k):
            drivers_dates[k] = []
        drivers_dates[k] += [dt]
    #
    for did, dates in drivers_dates.iteritems():
        ofpath = '%s%d.pkl' % (if_prefix, did)
        if check_path_exist(ofpath):
            continue
        dates.sort()
        dt_xy_state = []
        for dt in dates:
            yy = '%02d' % (dt.year - 2000)
            mm, dd = '%02d' % dt.month, '%02d' % dt.day
            yymmdd = yy + mm + dd
            ifpath = '%s/%s%s-%d.csv' % (if_dpath, if_prefix, yymmdd, did)
            with open(ifpath, 'rb') as logFile:
                reader = csv.reader(logFile)
                header = reader.next()
                # header: time,vehicle-id,driver-id,longitude,latitude,speed,state
                hid = {h: i for i, h in enumerate(header)}
                for row in reader:
                    dt = datetime.datetime.fromtimestamp(eval(row[hid['time']]))
                    lon, lat = map(eval, [row[hid[cn]] for cn in ['longitude', 'latitude']])
                    x, y = GPS_xyDrawing.convert_GPS2xy(lon, lat)
                    dt_xy_state += [dt, x, y, int(row[hid['state']])]
        save_pickle_file(ofpath, dt_xy_state)


def get_driver_trajectory(did):
    ofpath = '%s%d.pkl' % (if_prefix, did)
    if check_path_exist(ofpath):
        dt_xy_state = load_pickle_file(ofpath)
    else:
        dates = []
        for fn in get_all_files(if_dpath, '%s*.csv' % if_prefix):
            _, _date, _did = fn[:-len('.csv')].split('-')
            if int(_did) != did:
                continue
            year = 2000 + int(_date[:2])
            month, day = map(int, [_date[2:4], _date[4:6]])
            dt = datetime.datetime(year, month, day)
            dates += [dt]
        dates.sort()
        dt_xy_state = []
        for dt in dates:
            yy = '%02d' % (dt.year - 2000)
            mm, dd = '%02d' % dt.month, '%02d' % dt.day
            yymmdd = yy + mm + dd
            ifpath = '%s/%s%s-%d.csv' % (if_dpath, if_prefix, yymmdd, did)
            with open(ifpath, 'rb') as logFile:
                reader = csv.reader(logFile)
                header = reader.next()
                # header: time,vehicle-id,driver-id,longitude,latitude,speed,state
                hid = {h: i for i, h in enumerate(header)}
                for row in reader:
                    dt = datetime.datetime.fromtimestamp(eval(row[hid['time']]))
                    lon, lat = map(eval, [row[hid[cn]] for cn in ['longitude', 'latitude']])
                    x, y = GPS_xyDrawing.convert_GPS2xy(lon, lat)
                    dt_xy_state += [(dt, x, y, int(row[hid['state']]))]
        save_pickle_file(ofpath, dt_xy_state)
    return dt_xy_state


if __name__ == '__main__':
    print get_driver_trajectory(1)[:2]
    print get_driver_trajectory(32768)[:2]