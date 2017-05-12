import __init__
#
from information_boards import dpaths, prefixs
#
from taxi_common.file_handling_functions import get_all_files, check_path_exist
#
import csv


if_dpath = dpaths['qrTime_qNumber', 'ap']
if_prefix = prefixs['qrTime_qNumber', 'ap']


def run(yy):
    summary_fpath = '%s/%s20%s' % (if_dpath, if_prefix, yy)
    #
    for i, fn in enumerate(get_all_files(if_dpath, '%s%s*' % (if_prefix, yy))):
        fpath = '%s/%s' % (if_dpath, fn)
        with open(fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            if i == 0:
                with open(summary_fpath, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(header)
            for row in reader:





                prevEndTerminal, pickUpTerminal = (row[hid[cn]] for cn in ['prevEndTerminal', 'pickUpTerminal'])
                pickupTime = eval(row[hid['pickupTime']])
                duration, fare = map(eval, (row[hid[cn]] for cn in ['duration', 'fare']))
                prevTripEndTime = eval(row[hid['prevTripEndTime']])



        # process_daily(fpath)



if __name__ == '__main__':
    run('09')
