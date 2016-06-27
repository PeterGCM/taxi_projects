import __init__  # @UnresolvedImport # @UnusedImport
#
from b_aggregated_analysis.__init__ import ap_ep_dir, ap_ep_prefix
from b_aggregated_analysis.__init__ import ns_ep_dir, ns_ep_prefix
from b_aggregated_analysis.__init__ import Y09_ap_trips, Y10_ap_trips, Y09_ns_trips, Y10_ns_trips
#
import csv
#
def run():
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_files(yymm)

def process_files(yymm):
    print 'handle the file; %s' % yymm
    #
    ap_target_file = Y09_ap_trips if yymm.startswith('09') else Y10_ap_trips
    with open('%s/%s%s.csv' % (ap_ep_dir, ap_ep_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        if not os.path.exists(ap_target_file):
            with open(ap_target_file, 'wt') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(headers)
        with open(ap_target_file, 'a') as csvFile:
            writer = csv.writer(csvFile)
            for row in reader:
                writer.writerow(row)
    #
    ns_target_file = Y09_ns_trips if yymm.startswith('09') else Y10_ns_trips
    with open('%s/%s%s.csv' % (ns_ep_dir, ns_ep_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        if not os.path.exists(ns_target_file):
            with open(ns_target_file, 'wt') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(headers)
        with open(ns_target_file, 'a') as csvFile:
            writer = csv.writer(csvFile)
            for row in reader:
                writer.writerow(row)
    #
    print 'end the file; %s' % yymm
    
if __name__ == '__main__':
    run()