import __init__
#
import csv
#
from community_analysis._classes import ca_driver_with_distribution
from community_analysis import trip_dir, ld_dir
from community_analysis import generate_zones
from community_analysis import MIN_DAILY_LINKAGE
#
from taxi_common.file_handling_functions import save_pkl_threading, remove_create_dir, get_all_files, check_dir_create
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor



def run():
    check_dir_create(ld_dir)
    #
    init_multiprocessor(8)
    count_num_jobs = 0
    for mm in range(1,10):
        # yymm = '09%02d' % mm
        yymm = '12%02d' % mm
        # process_files(yymm)
        put_task(process_files, [yymm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
    print 'handle the file; %s' % yymm
    #
    linkage_yymm_dir = ld_dir + '/%s' % yymm
    remove_create_dir(linkage_yymm_dir)
    #
    out_boundary_logs_num = 0
    logs_num = 0
    out_boundary_logs_fn = linkage_yymm_dir + '/out_boundary.txt'
    with open(out_boundary_logs_fn, 'w') as f:
        f.write('time,did,i,j,zone_defined' + '\n')
    trip_yymm_dir = trip_dir + '/%s' % yymm
    for fn in get_all_files(trip_yymm_dir, '', '.csv'):
        drivers = {}
        zones = generate_zones()
        with open(trip_yymm_dir + '/%s' % fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            # {'i': 1, 'did': 3, ''j': 2, 'time': 0}
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                t = eval(row[hid['time']])
                did = row[hid['did']]
                # Find a targeted zone
                i, j = int(row[hid['si']]), int(row[hid['sj']])
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
                if not drivers.has_key(did): drivers[did] = ca_driver_with_distribution(did)
                drivers[did].update_linkage(t, z)
                logs_num += 1
        day_linkage = []
        for did0, d in drivers.iteritems():
            filtered_linkage = {}
            for did1, num_linkage in d.linkage.iteritems():
                if num_linkage < MIN_DAILY_LINKAGE:
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


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise