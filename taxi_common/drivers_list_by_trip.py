import __init__
#
from taxi_common import dl_by_trip_dir, dl_by_trip_prefix
from taxi_common import get_taxi_home_path
from file_handling_functions import remove_create_dir, save_pickle_file
from multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv


def run():
    remove_create_dir(dl_by_trip_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'handle the file; %s' % yymm
    yy, mm = yymm[:2], yymm[-2:]
    yyyy = str(2000 + int(yy))
    ext_file = get_taxi_home_path() + '/%s/%s/trips/trips-%s-normal-ext.csv' % (yyyy, mm, yymm)
    drivers = set()
    with open(ext_file, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
        hid = {h: i for i, h in enumerate(reader)}
        for row in reader:
            drivers.add(row[hid['driver-id']])
    save_pickle_file('%s/%s%s.pkl' % (dl_by_trip_dir, dl_by_trip_prefix, yymm), drivers)


if __name__ == '__main__':
    run()