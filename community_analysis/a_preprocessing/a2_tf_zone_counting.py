import __init__
#
from community_analysis import tf_zone_counting_dir, ft_trips_prefix
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv

def run():
    check_dir_create(tf_zone_counting_dir)
    #
    init_multiprocessor(6)
    count_num_jobs = 0
    for y in (9, 12):
        for m in range(1, 12):
            yymm = '%02d%02d' % (y, m)
            # yymm = '12%02d' % mm
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'Handle the file; %s' % yymm
    individual_count = {}
    with open('%s/%s%s.csv' % (all_trip_dir, all_trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            did = int(row[hid['did']])
            tf, zi, zj = int(row[hid['timeFrame']]), int(row[hid['zi']]), int(row[hid['zj']])
            if zi < 0 or zj < 0:
                continue
            if not year_individual_count.has_key(did):
                year_individual_count[did] = {}
                year_individual_count[did][hh, si, sj] = 0
            else:
                if not year_individual_count[did].has_key((hh, si, sj)):
                    year_individual_count[did][hh, si, sj] = 0
            year_individual_count[did][hh, si, sj] += 1

    save_pickle_file(individual_couting_fpath, year_individual_count)


if __name__ == '__main__':
    run()