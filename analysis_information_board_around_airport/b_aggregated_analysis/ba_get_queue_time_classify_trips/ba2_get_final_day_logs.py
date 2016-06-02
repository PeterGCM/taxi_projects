from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
import datetime, time, csv
from traceback import format_exc
#
from supports.etc_functions import remove_creat_dir, get_all_files
from supports._setting import logs_dir, log_last_day_dir
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor

def run():
    remove_creat_dir(log_last_day_dir)
    csv_files = get_all_files(logs_dir, '', '.csv')
    init_multiprocessor()
    count_num_jobs = 0
    for fn in csv_files:
        put_task(process_file, [fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
        
def process_file(fn):
    _, yymm = fn[:-len('.csv')].split('-')
    print 'handle the file; %s' % yymm 
    y, m = int('20' + yymm[:2]), int(yymm[2:])
    # find the next month's first day
    if m == 12:
        next_y, next_m = y + 1, 1 
    else:
        next_y, next_m = y, m + 1
    next_m_first_day = datetime.datetime(next_y, next_m, 1, 0)
    cur_m_last_day = next_m_first_day - datetime.timedelta(days=1)
    dd = '%2d' % cur_m_last_day.day
    last_day_timestamp = time.mktime(cur_m_last_day.timetuple())
    with open('%s/%s' % (logs_dir, fn), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_time = headers.index('time')
        with open('%s/log-last-day-%s%s.csv' % (log_last_day_dir, yymm, dd), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(headers)
            for row in reader:        
                t = eval(row[id_time])
                if t <= last_day_timestamp:
                    continue
                writer.writerow(row)
    print 'end the file; %s' % yymm
                
if __name__ == '__main__':
    run() 
