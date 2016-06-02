from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
#
from supports._setting import merged_trip_dir, trips_dir
from supports._setting import DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP
from supports._setting import DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS
from supports._setting import IN_NS, OUT_NS
from supports.etc_functions import remove_creat_dir, get_all_files
from supports.location_check import check_terminal_num, is_in_night_safari
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports.logger import logging_msg

def run():
    remove_creat_dir(trips_dir)
    csv_files = get_all_files(merged_trip_dir, 'trips', '.csv')
    #
    init_multiprocessor()
    counter = 0
    for fn in csv_files:
        counter += 1
        put_task(process_file, [fn])
    end_multiprocessor(counter)

def process_file(fn):
    _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm 
    logging_msg('handle the file; %s' % yymm)
    with open('%s/%s' % (merged_trip_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        #
        id_tid, id_vid, id_did = headers.index('trip-id'), headers.index('vehicle-id'), headers.index('driver-id')
        id_st, id_et = headers.index('start-time'), headers.index('end-time')
        id_dur, id_fare = headers.index('duration'), headers.index('fare')
        id_s_long, id_s_lat = headers.index('start-long'), headers.index('start-lat')
        id_e_long, id_e_lat = headers.index('end-long'), headers.index('end-lat')
        #
        vehicle_prev_trip_position_time = {}
        with open('%s/whole-trip-%s.csv' % (trips_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['tid', 'vid', 'did', 'start-time', 'end-time', 'duration', 'fare', 'ap-trip-mode', 'ns-trip-mode', 'prev-trip-end-time']
            writer.writerow(new_headers)
            for row in reader:
                vid = row[id_vid]
                start_time, end_time = eval(row[id_st]), eval(row[id_et]),
                s_long, s_lat = eval(row[id_s_long]), eval(row[id_s_lat])
                e_long, e_lat = eval(row[id_e_long]), eval(row[id_e_lat])
                #
                c_start_ter, c_end_ter = check_terminal_num(s_long, s_lat), check_terminal_num(e_long, e_lat)
                c_sl_ns, c_el_ns = is_in_night_safari(s_long, s_lat), is_in_night_safari(e_long, e_lat) 
                #
                if not vehicle_prev_trip_position_time.has_key(vid):
                    # ASSUMPTION
                    # If this trip is the driver's first trip in a month,
                    # let's assume that the previous trip occurred out of the airport and out of the night safari
                    # and also assume that the previous trip's end time is the current trip's start time 
                    # -1 represents out of airport zone
                    vehicle_prev_trip_position_time[vid] = (-1, OUT_NS, start_time)
                prev_trip_end_ter, prev_trip_end_loc_ns, prev_trip_time = vehicle_prev_trip_position_time[vid]
                ap_trip_mode, ns_trip_mode = None, None
                if prev_trip_end_ter != -1 and c_start_ter != -1 : ap_trip_mode = DInAP_PInAP
                elif prev_trip_end_ter != -1 and c_start_ter == -1: ap_trip_mode = DInAP_POutAP
                elif prev_trip_end_ter == -1 and c_start_ter != -1: ap_trip_mode = DOutAP_PInAP
                elif prev_trip_end_ter == -1 and c_start_ter == -1: ap_trip_mode = DOutAP_POutAP
                else: assert False
                #
                if prev_trip_end_loc_ns == IN_NS and c_sl_ns == IN_NS: ns_trip_mode = DInNS_PInNS
                elif prev_trip_end_loc_ns == IN_NS and c_sl_ns == OUT_NS: ns_trip_mode = DInNS_POutNS
                elif prev_trip_end_loc_ns == OUT_NS and c_sl_ns == IN_NS: ns_trip_mode = DOutNS_PInNS
                elif prev_trip_end_loc_ns == OUT_NS and c_sl_ns == OUT_NS: ns_trip_mode = DOutNS_POutNS   
                else: assert False
                
                new_row = [row[id_tid], vid, row[id_did],
                           start_time, end_time,
                           row[id_dur], row[id_fare],
                           ap_trip_mode, ns_trip_mode, prev_trip_time]
                writer.writerow(new_row)
                #
                vehicle_prev_trip_position_time[vid] = (c_end_ter, c_el_ns, end_time)
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()
