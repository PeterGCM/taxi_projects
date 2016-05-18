from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/..')
#
from supports.handling_pkl import load_picle_file
from supports.etc_functions import get_all_files, remove_creat_dir
from supports._setting import merged_trip_dir, for_full_driver_dir, individual_detail_dir
from supports.logger import logging_msg
from supports.location_check import is_in_airport
from supports._setting import OUT_AP
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
#
full_time_drivers, _, _, _, _, _, _, _, _, _, _ = load_picle_file('%s/productivities_ext.pkl' % (individual_detail_dir))
driver_full_or_not = [False] * (max(full_time_drivers) + 1)
for did in full_time_drivers:
    driver_full_or_not[int(did)] = True
check_progress = 10000000
#
def run():
    remove_creat_dir(for_full_driver_dir)
    init_multiprocessor()
    count_num_jobs = 0
    for fn in get_all_files(merged_trip_dir, 'trips', '.csv'):
#         process_file(fn)
        put_task(process_file, [fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_file(fn):
    _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    with open('%s/%s' % (merged_trip_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        #
        id_did = headers.index('driver-id')
        id_vid = headers.index('vehicle-id')
        id_st, id_et = headers.index('start-time'), headers.index('end-time')
        id_dur, id_fare = headers.index('duration'), headers.index('fare')
        id_s_long, id_s_lat = headers.index('start-long'), headers.index('start-lat')
        id_e_long, id_e_lat = headers.index('end-long'), headers.index('end-lat')
        #
        vehicle_prev_trip_position_time = {}
        with open('%s/full-drivers-trips-%s.csv' % (for_full_driver_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['did', 'prev-trip-end-time', 'prev-trip-end-location', 'start-time', 'start-location', 'end-time', 'end-location', 'duration', 'fare']
            writer.writerow(new_headers)
            count = 0
            for row in reader:
                did = int(row[id_did])
                if did > len(driver_full_or_not) or did < 0:
                    continue
                if not driver_full_or_not[did]:
                    continue
                vid = row[id_vid]
                start_time, end_time = eval(row[id_st]), eval(row[id_et]),
                s_long, s_lat = eval(row[id_s_long]), eval(row[id_s_lat])
                e_long, e_lat = eval(row[id_e_long]), eval(row[id_e_lat])
                s_location, e_location = is_in_airport(s_long, s_lat), is_in_airport(e_long, e_lat)
                #
                if not vehicle_prev_trip_position_time.has_key(vid):
                    # ASSUMPTION
                    # If this trip is the driver's first trip in a month,
                    # let's assume that the previous trip occurred out of the airport
                    # and also assume that the previous trip's end time is the current trip's start time 
                    vehicle_prev_trip_position_time[vid] = (OUT_AP, start_time)
                prev_trip_end_location, prev_trip_end_time = vehicle_prev_trip_position_time[vid]
                #
                new_row = [did, prev_trip_end_time, prev_trip_end_location, 
                           start_time, s_location,
                           end_time, e_location,
                           row[id_dur], row[id_fare]]
                writer.writerow(new_row)
                #
                vehicle_prev_trip_position_time[vid] = (e_location, end_time)
                #
                count +=1
                if count % check_progress == 0:
                    print '%s-----%d' % (yymm, count) 
                    logging_msg('%s-----%d' % (yymm, count))
    print 'end the file; %s' % yymm 
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()
