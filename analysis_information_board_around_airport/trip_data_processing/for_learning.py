from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
#
from supports.etc_functions import get_all_files, remove_creat_dir
from supports._setting import merged_trip_dir, for_learning_dir
from supports.location_check import is_in_airport
from supports._setting import OUT_AP
 
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor

def run():
    remove_creat_dir(for_learning_dir)
    csv_files = get_all_files(merged_trip_dir, 'trips', '.csv')
    #
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
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
        id_vid = headers.index('vehicle-id')
        id_st, id_et = headers.index('start-time'), headers.index('end-time')
        id_dur, id_fare = headers.index('duration'), headers.index('fare')
        id_s_long, id_s_lat = headers.index('start-long'), headers.index('start-lat')
        id_e_long, id_e_lat = headers.index('end-long'), headers.index('end-lat')
        #
        vehicle_prev_trip_position_time = {}
        with open('%s/whole-trip-%s.csv' % (for_learning_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['prev-trip-end-time', 'prev-trip-end-location', 'start-time', 'start-location', 'end-time', 'end-location', 'duration', 'fare']
            writer.writerow(new_headers)
            for row in reader:
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
                new_row = [prev_trip_end_time, prev_trip_end_location, 
                           start_time, s_location,
                           end_time, e_location,
                           row[id_dur], row[id_fare]]
                writer.writerow(new_row)
                #
                vehicle_prev_trip_position_time[vid] = (e_location, end_time)
    print 'end the file; %s' % yymm 
    logging_msg('end the file; %s' % yymm)
        
if __name__ == '__main__':
    run()
