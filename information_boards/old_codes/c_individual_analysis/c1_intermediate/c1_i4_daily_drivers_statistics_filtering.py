#
import csv

from information_boards.old_codes.c_individual_analysis import ftd_ap_daily_stat_filtered_fpath
from information_boards.old_codes.c_individual_analysis import ftd_ap_daily_stat_fpath


def run():
    with open(ftd_ap_daily_stat_filtered_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        #
        with open(ftd_ap_daily_stat_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            writer.writerow(headers)
            hid = {h: i for i, h in enumerate(headers)}
            reader.next()
            for row in reader:
                ap_num = int(row[hid['ap-num']])
                if ap_num == 0:
                    continue
                writer.writerow(row)


if __name__ == '__main__':
    run()
