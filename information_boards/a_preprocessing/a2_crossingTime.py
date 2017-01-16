import __init__
#
'''

'''
#
from information_boards import taxi_home
from information_boards import log_dpath, log_prefix
from information_boards import log_last_day_dpath, log_last_day_prefix
from information_boards import crossingTime_ap_dpath, crossingTime_ap_prefix
from information_boards import crossingTime_ns_dpath, crossingTime_ns_prefix
from information_boards import ap_poly_fn, ns_poly_fn
from information_boards import IN, OUT
#
from taxi_common.geo_functions import get_ap_polygons, get_ns_polygon
from taxi_common.file_handling_functions import check_path_exist, check_dir_create, get_all_files, save_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime, time


logger = get_logger()


def run():
    for dpath in [log_dpath, log_last_day_dpath, crossingTime_ap_dpath, crossingTime_ns_dpath]:
        check_dir_create(dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data_20160826 are corrupted
                continue
            put_task(log_location_labeling, [yymm])
            # put_task(log_last_day, [yymm])
            # put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    def record_crossing_time(path_to_csv_file,
                             veh_ap_crossing_time, veh_last_log_ap_or_not,
                             veh_ns_crossing_time, veh_last_log_ns_or_not):
        with open(path_to_csv_file, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                t, vid = eval(row[hid['time']]), row[hid['vid']]
                ap_or_not, ns_or_not = eval(row[hid['ap-or-not']]), eval(row[hid['ns-or-not']])
                #
                if not veh_last_log_ap_or_not.has_key(vid):
                    if ap_or_not == IN:
                        # the first log's position was occurred in the AP zone
                        assert not veh_ap_crossing_time.has_key(vid)
                        veh_ap_crossing_time[vid] = [t]
                else:
                    assert veh_last_log_ap_or_not.has_key(vid)
                    if veh_last_log_ap_or_not[vid] == OUT and ap_or_not == IN:
                        veh_ap_crossing_time.setdefault(vid, [t]).append(t)
                #
                if not veh_last_log_ns_or_not.has_key(vid):
                    if ns_or_not == IN:
                        # the first log's position was occurred in the NS zone
                        assert not veh_ns_crossing_time.has_key(vid)
                        veh_ns_crossing_time[vid] = [t]
                else:
                    assert veh_last_log_ns_or_not.has_key(vid)
                    if veh_last_log_ns_or_not[vid] == OUT and ns_or_not == IN:
                        veh_ns_crossing_time.setdefault(vid, [t]).append(t)
                #
                veh_last_log_ap_or_not[vid] = ap_or_not
                veh_last_log_ns_or_not[vid] = ns_or_not
        return veh_ap_crossing_time, veh_last_log_ap_or_not, veh_ns_crossing_time, veh_last_log_ns_or_not
    #
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        ap_pkl_fpath = '%s/%s%s.pkl' % (crossingTime_ap_dpath, crossingTime_ap_prefix, yymm)
        ns_pkl_fpath = '%s/%s%s.pkl' % (crossingTime_ns_dpath, crossingTime_ns_prefix, yymm)
        if check_path_exist(ap_pkl_fpath) and check_path_exist(ns_pkl_fpath):
            return None
        print 'handle the file; %s' % yymm
        veh_ap_crossing_time, veh_last_log_ap_or_not = {}, {}
        veh_ns_crossing_time, veh_last_log_ns_or_not = {}, {}
        if yymm not in ['0901', '1001', '1011']:
            y, m = int(yymm[:2]), int(yymm[2:])
            prev_m = m - 1
            prev_yymm = '%02d%02d' %(y, prev_m)
            prev_fn = get_all_files(log_last_day_dpath, '%s%s*.csv' % (log_last_day_prefix, prev_yymm))[0]
            path_to_last_day_csv_file = '%s/%s' % (log_last_day_dpath, prev_fn)
            veh_ap_crossing_time, veh_last_log_ap_or_not, veh_ns_crossing_time, veh_last_log_ns_or_not = \
                            record_crossing_time(path_to_last_day_csv_file, veh_ap_crossing_time, veh_last_log_ap_or_not,
                                                 veh_ns_crossing_time, veh_last_log_ns_or_not)
        path_to_csv_file = '%s/%s%s.csv' % (log_dpath, log_prefix, yymm)
        veh_ap_crossing_time, _, veh_ns_crossing_time, _ = \
                record_crossing_time(path_to_csv_file, veh_ap_crossing_time, veh_last_log_ap_or_not,
                                     veh_ns_crossing_time, veh_last_log_ns_or_not)
        #
        save_pickle_file(ap_pkl_fpath, veh_ap_crossing_time)
        save_pickle_file(ns_pkl_fpath, veh_ns_crossing_time)
        logger.info('end the file; %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


def log_location_labeling(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        log_fpath = '%s/%s%s.csv' % (log_dpath, log_prefix, yymm)
        if check_path_exist(log_fpath):
            logger.info('The file had already been processed; %s' % log_fpath)
            return
        yy, mm = yymm[:2], yymm[-2:]
        #
        ap_polygons, ns_polygon = get_ap_polygons(), get_ns_polygon()
        with open('%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open(log_fpath, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_headers = ['time', 'vid', 'did', 'ap-or-not', 'ns-or-not']
                writer.writerow(new_headers)
                #
                for row in reader:
                    _long, _lat = (eval(row[hid['longitude']]), eval(row[hid['latitude']]))
                    ap_or_not = False
                    for ap_polygon in ap_polygons:
                        if not ap_or_not:
                            res = ap_polygon.is_including((_long, _lat))
                            if res:
                                ap_or_not = res
                                break
                    np_or_not = ns_polygon.is_including((_long, _lat))
                    new_row = [row[hid['time']], row[hid['vehicle-id']], row[hid['driver-id']], ap_or_not, np_or_not]
                    writer.writerow(new_row)
        logger.info('end the file; %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


def log_last_day(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        y, m = int('20' + yymm[:2]), int(yymm[2:])
        # find the next month's first day
        if m == 12:
            next_y, next_m = y + 1, 1
        else:
            next_y, next_m = y, m + 1
        next_m_first_day = datetime.datetime(next_y, next_m, 1, 0)
        cur_m_last_day = next_m_first_day - datetime.timedelta(days=1)
        dd = '%02d' % cur_m_last_day.day
        ll_fpath = '%s/%s%s%s.csv' % (log_last_day_dpath, log_last_day_prefix, yymm, dd)
        if check_path_exist(ll_fpath):
            logger.info('The file had already been processed; %s' % ll_fpath)
            return
        #
        last_day_timestamp = time.mktime(cur_m_last_day.timetuple())
        log_fpath = '%s/%s%s.csv' % (log_dpath, log_prefix, yymm)

        with open(log_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open(ll_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(headers)
                for row in reader:
                    t = eval(row[hid['time']])
                    if t <= last_day_timestamp:
                        continue
                    writer.writerow(row)
        print 'end the file; %s' % yymm
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()
