import information_boards.b_aggregated_analysis.b1_intermediate
#
from information_boards.b_aggregated_analysis.b1_intermediate import HOUR1
from information_boards.b_aggregated_analysis import logs_dir, log_prefix
from information_boards.b_aggregated_analysis import logs_last_day_dir, log_last_day_prefix
#
from taxi_common.file_handling_functions import check_path_exist, get_all_files, get_created_time, check_dir_create
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import datetime, time, csv


def run():
    check_dir_create(logs_last_day_dir)
    #
    # init_multiprocessor(2)
    # count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data_20160826 are corrupted
                continue
            log_fpath = '%s/%s%s.csv' % (logs_dir, log_prefix, yymm)
            if (time.time() - get_created_time(log_fpath)) < HOUR1:
                continue
            process_file(yymm)
            # put_task(process_file, [yymm])
            # count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


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
    ll_fpath = '%s/%s%s%s.csv' % (logs_last_day_dir, log_last_day_prefix, yymm, dd)
    if check_path_exist(ll_fpath):
        return None
    #
    last_day_timestamp = time.mktime(cur_m_last_day.timetuple())
    with open('%s/%s%s.csv' % (logs_dir, log_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        with open(ll_fpath, 'wb') as w_csvfile:
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
