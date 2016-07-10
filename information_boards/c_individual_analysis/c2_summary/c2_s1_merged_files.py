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
def run():
    driver_measure = ['num-trips', 'fare', 'pro-dur', 'gen-prod', 
                      'pin-num-trips', 'pin-fare', 'pin-dur', 'pin-qu', 'pin-prod', 'pin-eco-profit',
                      'pout-num-trips', 'pout-fare', 'pout-dur', 'pout-qu', 'pout-prod', 'pout-eco-profit']
    for Y09_fn, Y10_fn in [(ftd_Y09_stat_ap_fn, ftd_Y10_stat_ap_fn), 
                           (ftd_Y09_stat_ns_fn, ftd_Y10_stat_ns_fn])]:
        remove_file(Y09_fn)
        remove_file(Y10_fn)
        #
        Y09_yymm, Y10_yymm = [], []
        for y in xrange(9, 11):
            for m in xrange(1, 13):
                yymm = '%02d%02d' % (y, m) 
                if yymm in ['0912', '1010']:
                    continue
                if yymm.startswith('09'):
                    Y09_yymm.append(yymm)
                else:
                    assert yymm.startswith('10')
                    Y10_yymm.append(yymm)
        for Y_yymm, Y_fn, stat_dir, stat_prefix in [(Y09_yymm, Y09_fn, ftd_stat_ap_trip_dir, ftd_stat_ap_trip_prefix),
                                                    (Y10_yymm, Y10_fn, ftd_stat_ns_trip_dir, ftd_stat_ns_trip_prefix)]:
            drivers = {}
            for yymm in Y_yymm:
                with open('%s/%s%s.csv' % (stat_dir, stat_prefix, yymm), 'rt') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    hid = {h : i for i, h in enumerate(headers)}
                    # 'did'
                    # 'num-trips', 'fare', 'pro-dur' 'gen-prod', 
                    # 'pin-num-trips', 'pin-fare', 'pin-dur', 'pin-qu', 'pin-prod', 'pin-eco-profit',
                    # 'pout-num-trips', 'pout-fare', 'pout-dur', 'pout-qu', 'pout-prod', 'pout-eco-profit'
                    for row in reader:
                        did = row[hid['did']]
                        if not drivers.has_key(did):
                            drivers[did] = [[] for _ in driver_measure]
                        for measure in driver_measure:
                            drivers[did][driver_measure.index(measure)].append(eval(row[hid[measure]]))
            with open(Y_fn, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                headers = ['did',
                           , 'num-trips', 'num-trips', 'num-trips', 
                           , 'fare', 
                           , 'pro-dur', 
                           , 'gen-prod', 
                           , 'pin-num-trips', 
                           , 'pin-fare', 
                           , 'pin-dur', 
                           , 'pin-qu', 
                           , 'pin-prod', 
                           , 'pin-eco-profit',
                           , 'pout-num-trips', 
                           , 'pout-fare', 
                           , 'pout-dur', 
                           , 'pout-qu', 
                           , 'pout-prod', 
                           , 'pout-eco-profit']

                            ]


                writer.writerow(headers)



def process_year(Y_yymm):

    dfs = pd.read_csv('%s/%s%s.csv' % (ap_ep_dir, ap_ep_prefix, yymm))

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