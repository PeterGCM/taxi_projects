import __init__
#
from __init__ import MIN_DAILY_LINKAGE, REMAINING_LINKAGE_RATIO
from _classes import cd_driver, cd_zone
from community_analysis.__init__ import log_dir, ld_dir
#
from taxi_common.file_handling_functions import save_pkl_threading, remove_create_dir, get_all_files
from taxi_common.singapore_grid_zone import get_singapore_zones
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv


def run():
    init_multiprocessor(6)
    count_num_jobs = 0
    for mm in range(1,12):
        put_task(process_files, ['09%02d' % mm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
    linkage_yymm_dir = ld_dir + '/%s' % yymm
    remove_create_dir(linkage_yymm_dir)
    #
    out_boundary_logs_num = 0
    logs_num = 0
    out_boundary_logs_fn = linkage_yymm_dir + '/out_boundary.txt'
    with open(out_boundary_logs_fn, 'w') as f:
        f.write('time,did,i,j,zone_defined' + '\n')
    log_yymm_dir = log_dir + '/%s' % yymm
    for fn in get_all_files(log_yymm_dir, '', '.csv'):
        drivers = {}
        zones = generate_zones()
        with open(log_yymm_dir + '/%s' % fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            # {'i': 1, 'did': 3, ''j': 2, 'time': 0}
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                t = eval(row[hid['time']])
                did = row[hid['did']]
                # Find a targeted zone
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
                except KeyError:
                    out_boundary_logs_num += 1
                    with open(out_boundary_logs_fn, 'a') as f:
                        f.write('%d,%s,%d,%d,X' % (t, did, i, j) + '\n')
                    continue
                #
                if not drivers.has_key(did): drivers[did] = cd_driver(did)
                drivers[did].update_linkage(t, z)
                logs_num += 1
        day_linkage = []
        for did0, d in drivers.iteritems():
            filtered_linkage = {}
            for did1, num_linkage in d.linkage.iteritems():
                if num_linkage < MIN_DAILY_LINKAGE or num_linkage < d.num_pickup * REMAINING_LINKAGE_RATIO:
                    continue
                filtered_linkage[did1] = num_linkage
            day_linkage.append((did0, d.num_pickup, filtered_linkage))
        save_pkl_threading(linkage_yymm_dir + '/%s.pkl' % fn[:-len('.csv')], day_linkage)
        for del_object in [day_linkage, zones, drivers]:
            del del_object
    with open(out_boundary_logs_fn, 'a') as f:
        f.write('the total number of logs: %d' % (logs_num) + '\n')
        f.write('the total number of out boundary logs: %d' % (out_boundary_logs_num) + '\n')

    from taxi_common.file_handling_functions import thread_writing
    if thread_writing:
        thread_writing.join()


def generate_zones():
    zones = {}
    basic_zones = get_singapore_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = cd_zone(z.relation_with_poly, z.i, z.j, z.x, z.y)
    return zones


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise