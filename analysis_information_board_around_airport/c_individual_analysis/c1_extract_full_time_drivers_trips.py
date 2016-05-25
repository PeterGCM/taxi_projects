from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import full_drivers_trips_dir, full_drivers_trips_prefix
from supports._setting import zero_duration_time_slots
from supports._setting import full_time_drivers_shift_dir, full_time_drivers_prefix
from supports._setting import GENERAL
from supports._setting import trips_dir, trip_prefix
from supports.etc_functions import load_picle_file
from supports.etc_functions import remove_creat_dir
#
import csv, datetime
#
omitted_timeslots = [] 
for l, ts in load_picle_file(zero_duration_time_slots):
    if l == GENERAL:
        yyyy, mm, dd, hh = 2000 + eval(ts[0]), eval(ts[1]), eval(ts[2]), eval(ts[3])
        omitted_timeslots.append((yyyy, mm, dd, hh))

def run():
    remove_creat_dir(full_drivers_trips_dir)
#     init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)
#             put_task(process_files, [yymm])
            count_num_jobs += 1
#     end_multiprocessor(count_num_jobs)

def process_files(yymm):
    print 'handle the file; %s' % yymm
    full_dids = sorted([int(eval(x)) for x in load_picle_file('%s/%s%s.pkl' % (full_time_drivers_shift_dir, full_time_drivers_prefix, yymm))])
    print full_dids
    
    assert False
    with open('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (full_drivers_trips_dir, full_drivers_trips_prefix, yymm), 'wt') as w_csvfile:
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
                did = int(eval(row[hid['did']]))
                if did not in full_dids:
                    continue
                writer.writerow([row[hid['did']],
                                 row[hid['start-time']],
                                 row[hid['duration']],
                                 row[hid['fare']]])
                        
if __name__ == '__main__':
    run()
