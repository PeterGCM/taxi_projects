import __init__  # @UnresolvedImport # @UnusedImport
#
from c_individual_analysis.__init__ import ftd_gen_stat_dir, ftd_gen_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix
from c_individual_analysis.__init__ import Y09_ftd_gen_stat, Y10_ftd_gen_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat
#
from taxi_common.file_handling_functions import remove_file, check_path_exist
#
import csv
#
_package = [(ftd_gen_stat_dir, ftd_gen_stat_prefix , Y09_ftd_gen_stat, Y10_ftd_gen_stat),
            (ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix, Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat),
            (ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix, Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat),
            (ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix, Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat),
            (ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix, Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat)]
#
def run():
    for _, _, Y09, Y10 in _package:
        remove_file(Y09)
        remove_file(Y10)
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
            if not check_path_exist(target_file):
                with open(target_file, 'wt') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(headers)
            with open(target_file, 'a') as csvFile:
                writer = csv.writer(csvFile)
                for row in reader:
                    writer.writerow(row)

if __name__ == '__main__':
    run()