import __init__
#
from community_analysis import ft_trips_dir, ft_trips_prefix
from community_analysis import tf_zone_counting_dir, ft_trips_prefix
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv


def run():
    check_dir_create(tf_zone_counting_dir)
    #
    init_multiprocessor(3)
    count_num_jobs = 0
    for y in (9, 10):
        for m in range(1, 12):
            yymm = '%02d%02d' % (y, m)
            # yymm = '12%02d' % mm
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'Handle the file; %s' % yymm
    drivers = {}
    with open('%s/%s%s.csv' % (ft_trips_dir, ft_trips_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            did = int(row[hid['did']])
            tf, zi, zj = int(row[hid['timeFrame']]), int(row[hid['i']]), int(row[hid['j']])
            if not drivers.has_key(did):
                drivers[did] = {}
                drivers[did][tf, zi, zj] = 0
            else:
                if not drivers[did].has_key((tf, zi, zj)):
                    drivers[did][tf, zi, zj] = 0
            drivers[did][tf, zi, zj] += 1
    save_pickle_file('%s/%s%s.pkl' % (tf_zone_counting_dir, ft_trips_prefix, yymm), drivers)


if __name__ == '__main__':
    run()