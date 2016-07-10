import __init__
#
from a_overall_analysis.__init__ import trips_dir, trip_prefix
from b_aggregated_analysis.__init__ import zero_duration_timeslots
from b_aggregated_analysis.__init__ import shift_pro_dur_dir, shift_pro_dur_prefix
from b_aggregated_analysis.__init__ import vehicle_sharing_dir, vehicle_sharing_prefix
from b_aggregated_analysis.b2_summary.__init__ import GENERAL
from c_individual_analysis.__init__ import ftd_trips_dir, ftd_trips_prefix
from c_individual_analysis.__init__ import ftd_shift_dir, ftd_shift_prefix
from c_individual_analysis.__init__ import ftd_list_dir, ftd_list_prefix
#
from taxi_common.file_handling_functions import load_pickle_file, remove_create_dir, save_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
omitted_timeslots = [] 
for l, ts in load_pickle_file(zero_duration_timeslots):
    if l == GENERAL:
        yyyy, mm, dd, hh = 2000 + eval(ts[0]), eval(ts[1]), eval(ts[2]), eval(ts[3])
        omitted_timeslots.append((yyyy, mm, dd, hh))


def run():
    for path in [ftd_trips_dir, ftd_shift_dir, ftd_list_dir]:
        remove_create_dir(path)

    init_multiprocessor()
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
    is_driver_vehicle = load_pickle_file('%s/%s%s.pkl' % (vehicle_sharing_dir, vehicle_sharing_prefix, yymm))
    full_time_drivers = set()
    with open('%s/%s%s.csv' % (shift_pro_dur_dir, shift_pro_dur_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (ftd_shift_dir, ftd_shift_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(headers)
            for row in reader:
                if len(is_driver_vehicle[row[hid['vid']]]) > 1:
                    continue
                writer.writerow(row)
                full_time_drivers.add(int(row[hid['did']]))
    #
    with open('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (ftd_trips_dir, ftd_trips_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['did', 'start-time', 'duration', 'fare']
            writer.writerow(new_headers)
            #
            # filter out trips data based on two factors;
            #   1. full time driver
            #   2. time slots when log data corrupted
            #
            for row in reader:
                st_ts = eval(row[hid['start-time']])
                st_dt = datetime.datetime.fromtimestamp(st_ts)
                k = (st_dt.year, st_dt.month, st_dt.day, st_dt.hour)
                if k in omitted_timeslots:
                    continue
                did = int(row[hid['did']])
                if did not in full_time_drivers:
                    continue
                writer.writerow([row[hid['did']],
                                 row[hid['start-time']],
                                 row[hid['duration']],
                                 row[hid['fare']]])
    #
    save_pickle_file('%s/%s%s.pkl' % (ftd_list_dir, ftd_list_prefix, yymm), list(full_time_drivers))
    print 'end the file; %s' % yymm

if __name__ == '__main__':
    run()
