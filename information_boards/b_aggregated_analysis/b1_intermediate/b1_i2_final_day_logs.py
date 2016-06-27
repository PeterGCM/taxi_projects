import __init__  # @UnresolvedImport # @UnusedImport
#
from b_aggregated_analysis.__init__ import logs_dir, log_prefix
from b_aggregated_analysis.__init__ import logs_last_day_dir, log_last_day_prefix
#
from taxi_common.file_handling_functions import remove_creat_dir, get_all_files
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import datetime, time, csv
#
def run():
    remove_creat_dir(logs_last_day_dir)
    #
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data are corrupted
                continue
            # process_files(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

def process_file(yymm):
    print 'handle the file; %s' % yymm
    y, m = int('20' + yymm[:2]), int(yymm[2:])
    # find the next month's first day
    if m == 12:
        next_y, next_m = y + 1, 1 
    else:
        next_y, next_m = y, m + 1
    next_m_first_day = datetime.datetime(next_y, next_m, 1, 0)
    cur_m_last_day = next_m_first_day - datetime.timedelta(days=1)
    dd = '%02d' % cur_m_last_day.day
    last_day_timestamp = time.mktime(cur_m_last_day.timetuple())
    with open('%s/%s%s.csv' % (logs_dir, log_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        with open('%s/%s%s%s.csv' % (logs_last_day_dir, log_last_day_prefix, yymm, dd), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(headers)
            for row in reader:        
                t = eval(row[hid['time']])
                if t <= last_day_timestamp:
                    continue
                writer.writerow(row)
    print 'end the file; %s' % yymm
                
if __name__ == '__main__':
    run() 
