from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import hourly_productivities, zero_duration_time_slots
from supports._setting import GENERAL
from supports._setting import Q_LIMIT_MIN
from supports._setting import airport_trips_dir, ap_trip_prefix
from supports._setting import ap_trips_economic_profits_dir, ap_trips_ecoprof_prefix
from supports.etc_functions import get_all_files, remove_creat_dir
from supports.etc_functions import load_picle_file
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
omitted_timeslots = [] 
for l, ts in load_picle_file(zero_duration_time_slots):
    if l == GENERAL:
        yyyy, mm, dd, hh = 2000 + eval(ts[0]), eval(ts[1]), eval(ts[2]), eval(ts[3])
        omitted_timeslots.append((yyyy, mm, dd, hh))

ap_out_productivities = {}
with open(hourly_productivities) as r_csvfile:
    reader = csv.reader(r_csvfile)
    headers = reader.next()
    hid = {h : i for i, h in enumerate(headers)}
    for row in reader:
        yyyy, mm, dd, hh = 2000 + eval(row[hid['yy']]), eval(row[hid['mm']]), eval(row[hid['dd']]), eval(row[hid['hh']])
        if (yyyy, mm, dd, hh) in omitted_timeslots:
            continue  
        ap_out_productivities[(yyyy, mm, dd, hh)] = eval(row[hid['ap-out-productivity']])

def run():
    remove_creat_dir(ap_trips_economic_profits_dir)
    csv_files = get_all_files(airport_trips_dir, ap_trip_prefix, '.csv')
    #
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
        put_task(process_file, [fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
#     
def process_file(fn):
    _, _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm 
    with open('%s/%s' % (airport_trips_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (ap_trips_economic_profits_dir, ap_trips_ecoprof_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile) 
            new_headers = ['did',
                           'start-time', 'yy', 'mm', 'dd', 'hh',
                           'duration', 'fare',
                           'ap-trip-mode', 'ap-queue-time',
                           'economic-profit']
            writer.writerow(new_headers)
            #
            # ASSUMPTION
            # opportunity costs are determined by start-time and duration,
            #  even though queue time and duration span more than two time slots
            # and also there are not much difference between consecutive time slots' productivities
            # 
            for row in reader:
                st_ts = eval(row[hid['start-time']])
                st_dt = datetime.datetime.fromtimestamp(st_ts)
                k = (st_dt.year, st_dt.month, st_dt.day, st_dt.hour)
                if k in omitted_timeslots:
                    continue
                qt = eval(row[hid['ap-queue-time']])
                if qt < Q_LIMIT_MIN:
                    qt = 0
                dur, fare = eval(row[hid['duration']]), eval(row[hid['fare']]) 
                eco_profit = fare - ap_out_productivities[k] * (qt + dur)

                writer.writerow([row[hid['did']],
                                 st_ts, st_dt.year - 2000, st_dt.month, st_dt.day, st_dt.hour,
                                 dur, fare,
                                 row[hid['ap-trip-mode']], qt,
                                 eco_profit])
    #
    print 'end the file; %s' % yymm
    
if __name__ == '__main__':
    run()
