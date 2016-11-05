import __init__
#
from information_boards.c_individual_analysis import ftd_ap_daily_stat_fpath
from information_boards.c_individual_analysis import ftd_ap_daily_stat_filtered_fpath
#
import csv


def run():
    with open(ftd_ap_daily_stat_filtered_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        headers = ['yy', 'mm', 'dd', 'did',
                   'all-num', 'all-dur', 'all-fare',
                   'ap-num', 'ap-dur', 'ap-fare', 'ap-ep', 'ap-queueing-time',
                   'apIn-num', 'apIn-dur', 'apIn-fare', 'apIn-ep', 'apIn-queueing-time',
                   'apOut-num', 'apOut-dur', 'apOut-fare', 'apOut-ep', 'apOut-queueing-time']
        writer.writerow(headers)
        #
        with open(ftd_ap_daily_stat_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                ap_num = int(row[hid['ap-num']])
                if ap_num == 0:
                    continue
                writer.writerow(row)


if __name__ == '__main__':
    run()
