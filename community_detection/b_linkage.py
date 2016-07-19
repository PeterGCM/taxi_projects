import __init__
#
from __init__ import logs_dir, linkage_dir
from __init__ import MIN_LINKAGE_NUM, MIN_LINKAGE_RATIO
from _classes import cd_driver, cd_zone
#
from taxi_common.file_handling_functions import save_pkl_threading, remove_create_dir, get_all_files
from taxi_common.singapore_grid_zone import get_singapore_zones
#
import csv


def run():
    # process_files('0902')
    handle_a_timeslot('20090116-1')


def handle_a_timeslot(yyyymmdd_t):
    yymm = yyyymmdd_t[len('20'):-len('dd-t')]
    linkage_yymm_dir = linkage_dir + '/%s' % yymm
    log_yymm_dir = logs_dir + '/%s' % yymm
    #
    drivers = {}
    zones = generate_zones()
    #
    out_boundary_logs_fn = linkage_yymm_dir + '/out_boundary_%s.txt' % yyyymmdd_t
    logs_num, out_boundary_logs_num = 0, 0
    with open(log_yymm_dir + '/%s.csv' % yyyymmdd_t, 'rb') as r_csvfile:
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
            if num_linkage < MIN_LINKAGE_NUM or num_linkage < MIN_LINKAGE_RATIO * d.num_pickup:
                continue
            filtered_linkage[did1] = num_linkage
        day_linkage.append((did0, d.num_pickup, filtered_linkage))
    save_pkl_threading(linkage_yymm_dir + '/%s.pkl' % yyyymmdd_t, day_linkage)
    #
    for del_object in [day_linkage, zones, drivers]:
        del del_object


def process_files(yymm):
    linkage_yymm_dir = linkage_dir + '/%s' % yymm
    remove_create_dir(linkage_yymm_dir)
    #
    out_boundary_logs_num = 0
    logs_num = 0
    out_boundary_logs_fn = linkage_yymm_dir + '/out_boundary.txt'
    with open(out_boundary_logs_fn, 'w') as f:
        f.write('time,did,i,j,zone_defined' + '\n')
    log_yymm_dir = logs_dir + '/%s' % yymm
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
                if num_linkage < MIN_LINKAGE_NUM or num_linkage < MIN_LINKAGE_RATIO * d.num_pickup:
                    continue
                filtered_linkage[did1] = num_linkage
            day_linkage.append((did0, d.num_pickup, filtered_linkage))
        save_pkl_threading(linkage_yymm_dir + '/%s.pkl' % fn[:-len('.csv')], day_linkage)
        #
        for del_object in [day_linkage, zones, drivers]:
            del del_object
    with open(out_boundary_logs_fn, 'a') as f:
        f.write('the total number of logs: %d' % (logs_num) + '\n')
        f.write('the total number of out boundary logs: %d' % (out_boundary_logs_num) + '\n')


def generate_zones():
    zones = {}
    basic_zones = get_singapore_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = cd_zone(z.relation_with_poly, z.i, z.j, z.x, z.y)
    return zones


if __name__ == '__main__':
    run()