import __init__
#
from taxi_common import shifts_dir, shift_prefix
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from file_handling_functions import remove_create_dir, save_pickle_file, check_dir_create
from multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, gzip


def run():
    # remove_create_dir(full_time_driver_dir)
    check_dir_create(full_time_driver_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    # for y in xrange(9, 11):
    #     for m in xrange(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         if yymm in ['0912', '1010']:
    #             continue
    #         # process_file(yymm)
    #         put_task(process_file, [yymm])
    #         count_num_jobs += 1

    for yymm in ['1101', '1106', '1107', '1108', '1109', '1111', '1112']:
        # process_file(yymm)
        put_task(process_file, [yymm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'handle the file; %s' % yymm
    vehicle_sharing = {}
    with gzip.open('%s/%s%s.csv.gz' % (shifts_dir, shift_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            vid, did = row[hid['vehicle-id']], row[hid['driver-id']]
            if not vehicle_sharing.has_key(vid):
                vehicle_sharing[vid] = set()
            vehicle_sharing[vid].add(did)
    one_shift_drivers = []
    for vid, drivers in vehicle_sharing.iteritems():
        if len(drivers) > 1:
            continue
        did = drivers.pop()
        assert len(drivers) == 0
        one_shift_drivers.append(did)
    save_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm), one_shift_drivers)


if __name__ == '__main__':
    run()