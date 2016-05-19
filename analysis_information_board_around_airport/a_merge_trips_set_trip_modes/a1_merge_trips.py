from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
import csv
from time import time, strftime
#
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
_log_txt = 'log.txt'
_stout = sys.stdout
_fix_time = time()
PERIOD = 30
X_LOGGING = False
#
TAXI_HOME = '/home/taxi'
USER_HOME = '/home/temp'
# YEARS = ['2009', '2010', '2011', '2012']
YEARS = ['2011', '2012']
MONTHS = ['01', '02', '03', '04', '05', '06',
          '07', '08', '09', '10', '11', '12']


def combine_trip_data_with_multi():
    '''
    In the server, when two files are combined, a trip can totally be expressed
    A trip data shows the below information;
    
    trip-id,job-id,start-time,end-time,start-long,start-lat,end-long,end-lat,vehicle-id,distance,fare,duration,start-dow,start-day,start-hour,start-minute,end-dow,end-day,end-hour,end-minute,start-zone,end-zone,start-postal,end-postal,driver-id
    
    ex.
    6029L09010100005,001010000,1230739200,1230739680,103.95029,1.37226,103.93417,1.38599,8069,3.4,850,480,4,1,0,0,4,1,0,8,51,51,518457,519355,20108
    
    Also, this function uses the multiprocess library in Python.
    '''
    
    logging_on_txt('Start combine!!', gen_txt=True)
    init_multiprocessor()
    print 'Start combine'
    for y in YEARS:
        y_two_digit = y[-2:]
        for m in MONTHS:
            normal_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal.csv' % (y, m, y_two_digit, m)
            ext_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal-ext.csv' % (y, m, y_two_digit, m)
            put_task(read_write_a_trip, [normal_file, ext_file])
    end_multiprocessor(len(YEARS) * len(MONTHS))

def read_write_a_trip(nf, ef):
    target_period = nf.split('/')[-1].split('-')[1]
    logging_on_txt('Handling trip-%s' % target_period)
    process_start_time = time()
    # Read data from files
    logging_on_txt('Read normal data-%s' % target_period)
    normal_data = csv_read_whole(nf)
    if normal_data == None:
        return None 
    #
    logging_on_txt('Read ext data-%s' % target_period)
    ext_data = csv_read_whole(ef)
    #
    assert len(normal_data) == len(ext_data), (target_period, len(normal_data), len(ext_data)) 
    # Write a combined file
    combined_file = USER_HOME + '/trips_merged/trips-%s.csv' % (target_period)
    logging_on_txt('Write a combined file-%s' % target_period)
    with open(combined_file, 'wt') as csvfile:
        writer = csv.writer(csvfile)
        for i in xrange(len(normal_data)):
            writer.writerow(normal_data[i] + ext_data[i])
    del normal_data, ext_data  
    logging_on_txt('Finish handiling trip-%s; t: %.2f' % (target_period, time() - process_start_time)) 
            
def csv_read_whole(fn):
    rv = []
    try:
        with open(fn, 'rt') as csvfile:
            reader = csv.reader(csvfile)
            i = 0 
            for row in reader:
                rv.append(row)
                i += 1
    except IOError:
        with open(_log_txt, 'w') as f:
            f.write(strftime("%a, %d %b %Y %H:%M:%S---") + '%s dese not exist' % fn + '\n')
            return None
    return rv

def logging_on_txt(s, gen_txt=False):
    global X_LOGGING
    if X_LOGGING:
        return
    if gen_txt:
        if os.path.exists(_log_txt): os.remove(_log_txt)
        with open(_log_txt, 'w') as f:
            f.write(strftime("%a, %d %b %Y %H:%M:%S---") + s + '\n')
    else:
        with open(_log_txt, 'a') as f:
            f.write(strftime("%a, %d %b %Y %H:%M:%S---") + s + '\n')

def test_single_run():
    normal_file = TAXI_HOME + '/2009/01/trips/trips-0901-normal.csv'
    ext_file = TAXI_HOME + '/2009/01/trips/trips-0901-normal-ext.csv'
    read_write_a_trip(normal_file, ext_file)

def combine_trip_data():
    print 'Start combine'
    for y in YEARS:
        y_two_digit = y[-2:]
        for m in MONTHS:
            if os.path.exists(USER_HOME + '/taxi/trips/trips-%s%s.csv' % (y_two_digit, m)):
                continue
            normal_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal.csv' % (y, m, y_two_digit, m)
            ext_file = TAXI_HOME + '/%s/%s/trips/trips-%s%s-normal-ext.csv' % (y, m, y_two_digit, m)
            read_write_a_trip(normal_file, ext_file)

if __name__ == '__main__':
    '''
    just test!!
    '''
    
#     from shapely.geometry import Polygon
#     print 'test!!'
#     test_single_run()
#     combine_trip_data_with_multi()
    combine_trip_data()
    