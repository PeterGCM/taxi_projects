import __init__
#
'''

'''
#
from information_boards.c_individual_analysis import ssd_apIn_fpath
from information_boards.b_aggregated_analysis import ap_ep_dir, ap_ep_prefix
#
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import csv

logger = get_logger()


def run():
    with open(ssd_apIn_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        headers = ['timeStamp', 'did', 'duration', 'fare',
                   'year', 'month',
                   'apIn', 'apQTime']
        writer.writerow(headers)
    for m in xrange(1, 13):
        yymm = '10%02d' % (m)
        if yymm in ['1010']:
            continue
        ft_drivers = map(int, load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm)))
        ap_ep_fpath = '%s/%s%s.csv' % (ap_ep_dir, ap_ep_prefix, yymm)
        with open(ap_ep_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                t = eval(row[hid['time']])
                cur_dt = datetime.datetime.fromtimestamp(t)
                if handling_day != cur_dt.day:





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
