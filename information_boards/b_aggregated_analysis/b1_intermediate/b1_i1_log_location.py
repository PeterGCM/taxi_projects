import __init__
#
from information_boards.b_aggregated_analysis import logs_dir, log_prefix
from information_boards import taxi_home
from information_boards import ap_poly, ns_poly
#
from taxi_common.file_handling_functions import remove_create_dir, check_path_exist, check_dir_create
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv


def run():
    check_dir_create(logs_dir)
    #
    init_multiprocessor(8)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                # both years data_20160826 are corrupted
                continue
            # process_files(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    fpath = '%s/%s%s.csv' % (logs_dir, log_prefix, yymm)
    if check_path_exist(fpath):
        return None


    print 'handle the file; %s' % yymm
    yy, mm = yymm[:2], yymm[-2:]
    #
    with open('%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        with open(fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['time', 'vid', 'did', 'ap-or-not', 'ns-or-not']
            writer.writerow(new_headers)
            #
            for row in reader:
                ap_or_not = ap_poly.is_including((eval(row[hid['longitude']]), eval(row[hid['latitude']])))
                np_or_not = ns_poly.is_including((eval(row[hid['longitude']]), eval(row[hid['latitude']])))
                new_row = [row[hid['time']], row[hid['vehicle-id']], row[hid['driver-id']], ap_or_not, np_or_not]
                writer.writerow(new_row)
    print 'end the file; %s' % yymm

if __name__ == '__main__':
    run()
