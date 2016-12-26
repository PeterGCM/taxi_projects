import __init__
#
'''

'''
#
from information_boards import shift_dpath, shift_prefix
from information_boards import productivity_dpath, productivity_prefix
from information_boards import shiftProDur_dpath, shiftProDur_prefix
from information_boards import AM2, AM5
#
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv, gzip

logger = get_logger()


def run():
    for dpath in [productivity_dpath, shiftProDur_dpath]:
        check_dir_create(dpath)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m)
            if yymm in ['0912', '1010']:
                continue
            # process_file(yymm)
            put_task(productive_duration, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def productive_duration(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        productive_state = ['dur%d' % x for x in [0, 3, 4, 5, 6, 7, 8, 9, 10]]
        with gzip.open('%s/%s%s.csv.gz' % (shift_dpath, shift_prefix, yymm), 'rt') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            with open('%s/%s%s.csv' % (shiftProDur_dpath, shiftProDur_prefix, yymm), 'wb') as w_csvfile:
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
        logger.info('end the file; %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
