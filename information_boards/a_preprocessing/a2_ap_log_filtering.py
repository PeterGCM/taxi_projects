import __init__
#
from information_boards import dpaths, prefixs
from information_boards import AM2, AM5
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
#
from datetime import datetime
import csv
#
if_dpath = dpaths['log']
if_prefixs = prefixs['log']
#
of_dpath = dpaths['log', 'ap']
of_prefixs = prefixs['log', 'ap']

try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(yymm):
    # consider only transition instances
    ifpath = '%s/%s%s.csv' % (if_dpath, if_prefixs, yymm)
    ofpath = None
    handling_day = 0
    vid_lastLoc = {}
    with open(ifpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            t = eval(row[hid['time']])
            dt = datetime.fromtimestamp(t)
            if dt.day == 1 and dt.hour <= AM5:
                continue
            if AM2 <= dt.hour and dt.hour <= AM5:
                continue
            if dt.day != handling_day and dt.hour == AM5 + 1:
                handling_day = dt.day
                ofpath = '%s/ap-%s%s%02d.csv' % (of_dpath, of_prefixs, yymm, handling_day)
                with open(ofpath, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_headers = ['time', 'vid', 'did', 'apBasePos']
                    writer.writerow(new_headers)
            vid, apBasedPos = int(row[hid['time']]), row[hid['apBasePos']]
            if vid_lastLoc.has_key(vid):
                if vid_lastLoc[vid] != apBasedPos:
                    with open(ofpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        writer.writerow(row)
                    vid_lastLoc[vid] = apBasedPos
            else:
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(row)
                vid_lastLoc[vid] = apBasedPos


if __name__ == '__main__':
    run('0901')