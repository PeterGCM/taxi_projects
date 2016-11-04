import __init__
#
from information_boards.c_individual_analysis import ftd_trips_dir, ftd_trips_prefix
from information_boards.c_individual_analysis import ftd_shift_dir, ftd_shift_prefix
from information_boards.b_aggregated_analysis import shift_pro_dur_dir, shift_pro_dur_prefix
from information_boards.a_overall_analysis import trips_dpath, trip_prefix
#
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file, remove_create_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime


def run():
    for path in [ftd_trips_dir, ftd_shift_dir]:
        remove_create_dir(path)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
#             process_files(yymm)
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
    print 'handle the file; %s' % yymm
    ft_drivers = load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm))
    with open('%s/%s%s.csv' % (shift_pro_dur_dir, shift_pro_dur_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (ftd_shift_dir, ftd_shift_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(headers)
            for row in reader:
                did = row[hid['did']]
                if did not in ft_drivers:
                    continue
                writer.writerow(row)
    #
    with open('%s/%s%s.csv' % (trips_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (ftd_trips_dir, ftd_trips_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['did', 'start-time', 'duration', 'fare', 'yy', 'mm', 'dd', 'hh']
            writer.writerow(new_headers)
            #
            # filter out trips data based on two factors;
            #   1. full time driver
            #
            for row in reader:
                st_ts = eval(row[hid['start-time']])
                st_dt = datetime.datetime.fromtimestamp(st_ts)
                did = row[hid['did']]
                if did not in ft_drivers:
                    continue
                writer.writerow([row[hid['did']],
                                 row[hid['start-time']],
                                 row[hid['duration']],
                                 row[hid['fare']], st_dt.year - 2000, st_dt.month, st_dt.day, st_dt.hour])
    #
    print 'end the file; %s' % yymm

if __name__ == '__main__':
    run()
