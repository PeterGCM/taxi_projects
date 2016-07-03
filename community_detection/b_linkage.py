import __init__
#
from __init__ import MEMORY_MANAGE_INTERVAL, COINCIDENCE_THRESHOLD_VALUE
from __init__ import POB, SIX_HOUR, EIGHT_HOUR
from __init__ import out_boundary_logs_fn, linkage_dir
from _classes import cd_driver
#
from taxi_common.file_handling_functions import save_pkl_threading, remove_creat_dir
#
import csv, datetime


def run(processed_log_fn, zones):
    _, time_from, time_to = processed_log_fn[:-len('.csv')].split('-')
    pkl_dir = linkage_dir + '/%s-%s' % (time_from[:len('yyyymmdd')], time_to[:len('yyyymmdd')])
    remove_creat_dir(pkl_dir)
    #
    out_boundary_logs_num = 0
    with open(out_boundary_logs_fn, 'w') as f:
        f.write('time,did,i,j,zone_defined' + '\n')
    #
    drivers = {}
    with open(processed_log_fn, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        # {'i': 1, 'did': 3, ''j': 2, 'time': 0}
        hid = {h: i for i, h in enumerate(headers)}
        memory_manage_clock = -1e400
        yyyy = eval(time_from[:len('yyyy')])
        mm = eval(time_from[len('yyyy'):len('yyyymm')])
        dd = eval(time_from[len('yyyymm'):len('yyyymmdd')])
        hh = eval(time_from[len('yyyymmdd'):len('yyyymmddhh')])
        handling_time = datetime.datetime(yyyy, mm, dd,hh)
        for row in reader:
            did = row[hid['did']]
            if did == '-1':
                continue
            t = eval(row[hid['time']])
            cur_time = datetime.datetime.fromtimestamp(t)
            if handling_time.hour + EIGHT_HOUR < cur_time.hour:
                day_linkage = []
                for did, d in drivers.iteritems():
                    day_linkage.append((did, d.linkage))
                #
                path = pkl_dir + '/%d%02d%02d-%d.pkl' % (handling_time.year, handling_time.month, handling_time.day, int(handling_time.hour / EIGHT_HOUR))
                save_pkl_threading(path, day_linkage)
                del day_linkage
                #
                handling_time = cur_time
                for z in zones.itervalues():
                    z.init_logQ()
                for did in drivers.iterkeys():
                    d = drivers.pop(did)
                    del d
            #
            # Find a targeted zone
            #
            i, j = int(row[hid['i']]), int(row[hid['j']])
            try:
                z = zones[(i, j)]
                #
                try:
                    assert z.check_validation()
                except AssertionError:
                    out_boundary_logs_num += 1
                    with open(out_boundary_logs_fn, 'a') as f:
                        f.write('%d,%s,%d,%d,O' % (t, did, i, j) + '\n')
                    continue
                out_boundary_logs_num += 1
            except KeyError:
                with open(out_boundary_logs_fn, 'a') as f:
                    f.write('%d,%s,%d,%d,X' % (t, did, i, j) + '\n')
                continue
            #
            if not drivers.has_key(did): drivers[did] = cd_driver(did)
            drivers[did].update_linkage(t, z)
