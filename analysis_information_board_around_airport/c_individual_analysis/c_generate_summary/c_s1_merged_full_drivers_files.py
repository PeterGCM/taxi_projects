from __future__ import division
#
import os, sys  
sys.path.append(os.getcwd() + '/../..')
#
from supports.etc_functions import check_dir_create
from supports._setting import summary_dir
from supports._setting import ftd_general_stat_dir, ftd_general_stat_prefix
from supports._setting import ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix
from supports._setting import ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix
from supports._setting import ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix
from supports._setting import ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix
#
from supports._setting import Y09_ftd_general_stat, Y10_ftd_general_stat
from supports._setting import Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat
from supports._setting import Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat
from supports._setting import Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat
from supports._setting import Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat
#
import csv
#
_package = [
#             (ftd_general_stat_dir, ftd_general_stat_prefix, Y09_ftd_general_stat, Y10_ftd_general_stat),
#            (ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix, Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat),
           (ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix, Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat),
#            (ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix, Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat),
           (ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix, Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat)]

def run():
    check_dir_create(summary_dir)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)

def process_files(yymm):
    print 'handle the file; %s' % yymm
    #
    for dn, fn_prefix, Y09, Y10 in _package:
        target_file = Y09 if yymm.startswith('09') else Y10
        with open('%s/%s%s.csv' % (dn, fn_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            if not os.path.exists(target_file):
                with open(target_file, 'wt') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(headers)
            with open(target_file, 'a') as csvFile:
                writer = csv.writer(csvFile)
                for row in reader:
                    writer.writerow(row)

if __name__ == '__main__':
    run()