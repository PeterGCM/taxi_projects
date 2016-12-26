#
import csv
import gzip

from information_boards import AM2, AM5
from information_boards.old_codes.b_aggregated_analysis import shift_pro_dur_dir, shift_pro_dur_prefix
from information_boards.old_codes.b_aggregated_analysis import shifts_dir, shift_prefix
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor


def run():
    check_dir_create(shift_pro_dur_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    print 'handle the file; %s' % yymm
    #        
    vehicle_sharing = {}
    productive_state = ['dur%d' % x for x in [0, 3, 4, 5, 6, 7, 8, 9, 10]]
    with gzip.open('%s/%s%s.csv.gz' % (shifts_dir, shift_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h : i for i, h in enumerate(headers)}
        with open('%s/%s%s.csv' % (shift_pro_dur_dir, shift_pro_dur_prefix, yymm), 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['yy', 'mm', 'dd', 'hh', 'vid', 'did', 'pro-dur']
            writer.writerow(new_headers)
            for row in reader:
                vid, did = row[hid['vehicle-id']], row[hid['driver-id']]
                #
                # Only consider trips whose start time is before 2 AM and after 6 AM
                #
                hh = eval(row[hid['hour']])
                if AM2 <= hh and hh <= AM5:
                    continue
                #
                productive_duration = sum(int(row[hid[dur]]) for dur in productive_state)
                writer.writerow([row[hid['year']][-2:], row[hid['month']], row[hid['day']], row[hid['hour']],
                                 vid, did, productive_duration])
    print 'end the file; %s' % yymm
    
if __name__ == '__main__':
    run()
