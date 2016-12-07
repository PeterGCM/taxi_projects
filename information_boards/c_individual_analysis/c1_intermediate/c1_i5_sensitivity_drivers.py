import __init__
#
'''

'''
#
from information_boards.c_individual_analysis import ssd_apIn_fpath
from information_boards.b_aggregated_analysis import ap_ep_dir, ap_ep_prefix
from information_boards import DIn_PIn
#
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime

logger = get_logger()


def run():
    with open(ssd_apIn_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        headers = ['timeStamp', 'did', 'duration', 'fare',
                   'year', 'month',' day', 'hour'
                   'apIn', 'apQTime']
        writer.writerow(headers)
    for m in xrange(1, 13):
        yymm = '10%02d' % m
        if yymm in ['1010']:
            continue
        logger.info('Start handling; %s' % yymm)
        ft_drivers = map(int, load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm)))
        ap_ep_fpath = '%s/%s%s.csv' % (ap_ep_dir, ap_ep_prefix, yymm)
        with open(ap_ep_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            handling_day = 0
            for row in reader:
                did = int(row[hid['did']])
                if did not in ft_drivers:
                    continue
                t = eval(row[hid['start-time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                if handling_day != cur_dt.day:
                    logger.info('...ing; %s(%dth)' % (yymm, handling_day))
                apIn = 1 if int(row[hid['trip-mode']]) == DIn_PIn else 0
                new_row = [
                    t, did, row[hid['duration']], row[hid['fare']],
                    row[hid['yy']], row[hid['mm']], row[hid['dd']], row[hid['hh']],
                    apIn, row[hid['queueing-time']]
                ]


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        import sys
        with open('___error_%s.txt' % (sys.argv[0]), 'w') as f:
            f.write(format_exc())
        raise
