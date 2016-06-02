from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
import csv
#
from supports._setting import logs_dir
from supports.etc_functions import remove_creat_dir
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports.location_check import is_in_airport, is_in_night_safari

TARGET_YEARS = ['2009', '2010']
server_prefix = '/home/taxi'
# server_prefix = '/Users/JerryHan88/taxi'

def run():
    remove_creat_dir(logs_dir)
    csv_file_paths = []
    for yd in os.listdir(server_prefix):
        yd_path = '%s/%s' % (server_prefix, yd)
        if not (os.path.isdir(yd_path) and yd.startswith('20')):
            continue
        if yd not in TARGET_YEARS:
            continue
        for md in os.listdir(yd_path):
            md_path = '%s/%s' % (yd_path, md)
            if not os.path.isdir(md_path):
                continue
            fn = 'logs-%s%s-normal.csv' % (yd[-2:], md)
            csv_file_paths.append('%s/%s/%s' % (md_path, 'logs', fn))
    init_multiprocessor()
    count_num_jobs = 0
    for path_to_csv_file in csv_file_paths:
#         process_file(path_to_csv_file)
        put_task(process_file, [path_to_csv_file])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)     

def process_file(path_to_csv_file):
    print path_to_csv_file
    ori_log_fn = path_to_csv_file.split('/')[-1]
    _, yymm, _ = ori_log_fn.split('-')
    print 'handle the file; %s' % yymm 
    with open(path_to_csv_file, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_time, id_vid, id_did = headers.index('time'), headers.index('vehicle-id'), headers.index('driver-id')
        index_long, index_lat = headers.index('longitude'), headers.index('latitude')
        with open('%s/log-%s.csv' % (logs_dir, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['time', 'vid', 'did', 'ap-or-not', 'np-or-not']
            writer.writerow(new_headers)
            #
            for row in reader:        
                ap_or_not = is_in_airport(eval(row[index_long]), eval(row[index_lat]))
                np_or_not = is_in_night_safari(eval(row[index_long]), eval(row[index_lat]))
                new_row = [row[id_time], row[id_vid], row[id_did], ap_or_not, np_or_not]
                writer.writerow(new_row)
    print 'end the file; %s' % yymm

if __name__ == '__main__':
    run()
