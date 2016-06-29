import __init__
#
from __init__ import MEMORY_MANAGE_INTERVAL, COINCIDENCE_THRESHOLD_VALUE
from __init__ import POB
from __init__ import out_boundary_logs_fn, linkage_dir
from _classes import cd_driver
#
from taxi_common.file_handling_functions import save_pickle_file, remove_creat_dir
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
        tf_date = datetime.date(yyyy, mm, dd)
        handling_date = tf_date
        pkl_fn = None
        for row in reader:
            t = eval(row[hid['time']])
            cur_date = datetime.date.fromtimestamp(t)
            if handling_date < cur_date:
                save_pickle_file(pkl_dir + '/%d%d%d' % (handling_date.year, handling_date.month, handling_date.day),
                                 [(did, d.linkage) for did, d in drivers.iteritems()])
                handling_date = cur_date
            did = row[hid['did']]
            i, j = int(row[hid['i']]), int(row[hid['j']])
            #
            # Find a targeted zone
            #
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
            except KeyError:
                out_boundary_logs_num += 1
                with open(out_boundary_logs_fn, 'a') as f:
                    f.write('%d,%s,%d,%d,X' % (t, did, i, j) + '\n')
                continue
            #
            if not drivers.has_key(did): drivers[did] = cd_driver(did)
            drivers[did].update_linkage(t, z)

            # if t - memory_manage_clock > MEMORY_MANAGE_INTERVAL:
            #     #
            #     # Remove low possibility relations
            #     #
            #     for d in drivers.itervalues():
            #         for d1, num in d.relation.iteritems():
            #             if num < COINCIDENCE_THRESHOLD_VALUE:
            #                 d.relation.pop(d1)
            #     memory_manage_clock = t

