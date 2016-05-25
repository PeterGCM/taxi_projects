from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
#
from supports._setting import shift_pro_dur_dir, shift_pro_dur_prefix
from supports._setting import vehicle_drivers_dir, vehicle_drivers_prefix
from supports._setting import full_time_drivers_shift_dir
from supports._setting import full_time_drivers_shift_prefix, full_time_drivers_prefix
from supports.etc_functions import remove_creat_dir, get_all_files
from supports.etc_functions import save_pickle_file, load_picle_file
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor

def run():
    remove_creat_dir(full_time_drivers_shift_dir)
    #
    csv_files = get_all_files(shift_pro_dur_dir, shift_pro_dur_prefix, '.csv')
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
        put_task(process_file, [fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_file(fn):
    _, _, _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm
    #
    is_driver_vehicle = load_picle_file('%s/%s%s.pkl' % (vehicle_drivers_dir, vehicle_drivers_prefix, yymm))
    full_drivers = set()
    with open('%s/%s' % (shift_pro_dur_dir, fn), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (full_time_drivers_shift_dir, full_time_drivers_shift_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(headers)
            for row in reader:
                if len(is_driver_vehicle[row[hid['vid']]]) > 1:
                    continue
                writer.writerow(row)
                full_drivers.add(row[hid['did']])
    save_pickle_file('%s/%s%s.pkl' % (full_time_drivers_shift_dir, full_time_drivers_prefix, yymm), full_drivers)
    print 'end the file; %s' % yymm
    
if __name__ == '__main__':
    run()
