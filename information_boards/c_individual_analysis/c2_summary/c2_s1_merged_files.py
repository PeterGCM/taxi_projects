import __init__
#
from c_individual_analysis.__init__ import ftd_stat_ap_trip_dir, ftd_stat_ap_trip_prefix
from c_individual_analysis.__init__ import ftd_stat_ns_trip_dir, ftd_stat_ns_trip_prefix
from c_individual_analysis.__init__ import ftd_Y09_stat_ap_fn, ftd_Y10_stat_ap_fn
from c_individual_analysis.__init__ import ftd_Y09_stat_ns_fn, ftd_Y10_stat_ns_fn




#
from taxi_common.file_handling_functions import remove_file, check_path_exist
#
import csv
#


_package = [(ftd_stat_ap_trip_dir, ftd_stat_ap_trip_prefix, ftd_Y09_stat_ap_fn, ftd_Y10_stat_ap_fn),
            (ftd_stat_ns_trip_dir, ftd_stat_ns_trip_prefix, ftd_Y09_stat_ns_fn, ftd_Y10_stat_ns_fn)]

def run():
    for _, _, Y09_fn, Y10_fn in _package:
        remove_file(Y09_fn)
        remove_file(Y10_fn)
        #
        Y09_yymm, Y10_yymm = [], []
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