from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports.etc_functions import remove_creat_dir, get_all_files
from supports._setting import shifts_dir, shift_pro_dur_dir
from supports.handling_pkl import save_pickle_file
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
#
def run():
    remove_creat_dir(shift_pro_dur_dir)
    init_multiprocessor()
    count_num_jobs = 0
    for fn in get_all_files(shifts_dir, 'shift-hour-state-', '.csv'):
        put_task(process_file, [fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_file(fn):
    _, _, _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    #        
    driver_vehicle = {}
    productive_state = ['dur%d' % x for x in [0, 3, 4, 5, 6, 7, 8, 9, 10]]
    with open('%s/%s' % (shifts_dir, fn), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/shift-pro-dur-%s.csv' % (shift_pro_dur_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['yy', 'mm', 'dd', 'hh', 'vid', 'did', 'pro-dur']
            writer.writerow(new_headers)
            for row in reader:
                vid, did = row[hid['vehicle-id']], row[hid['driver-id']]
                productive_duration = sum(int(row[hid[dur]]) for dur in productive_state)
                writer.writerow([row[hid['year']][-2:], row[hid['month']], row[hid['day']], row[hid['hour']],
                                 vid, did, productive_duration])
                driver_vehicle.setdefault(vid, set()).add(did)
    save_pickle_file('%s/driver-vehicle-%s.pkl' % (shifts_dir, yymm), driver_vehicle)
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)
    
if __name__ == '__main__':
    run()
