from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import full_shift_dir, trips_dir, airport_trips_dir, individual_detail_dir
from supports._setting import DInAP_PInAP, DOutAP_PInAP
from supports.etc_functions import remove_creat_dir
from supports.etc_functions import load_picle_file
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports.logger import logging_msg
#
import csv
import pandas as pd
from traceback import format_exc
#
sh_full_prefix, trip_prefix, ap_trip_op_ep_prefix = 'shift-full-time-', 'whole-trip-', 'ap-trip-op-ep-'
monthly_full_did_prefix = 'full-time-drivers-'
general_prefix, prev_in_ap_prefix, prev_out_ap_prefix = 'individual-general-', 'individual-prev-in-ap-', 'individual-prev-out-ap-'
#
SEC = 60
#
def run():
    remove_creat_dir(individual_detail_dir)
#     process_files('1007')
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            try:
                yymm = '%02d%02d' % (y, m) 
                if yymm in ['0912', '1010']:
                    continue
                put_task(process_files, [yymm])
            except Exception as _:
                logging_msg('Algorithm runtime exception (%s)\n' % (yymm) + format_exc())
                raise
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    #
    init_csv_files(yymm)
    #
    full_dids = sorted([eval(x) for x in load_picle_file('%s/%s%s.pkl' % (full_shift_dir, monthly_full_did_prefix, yymm))])
    s_df = pd.read_csv('%s/%s%s.csv' % (full_shift_dir, sh_full_prefix, yymm))
    trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
    ap_trip_df = pd.read_csv('%s/%s%s.csv' % (airport_trips_dir, ap_trip_op_ep_prefix, yymm))
    #
    yy, mm = int(yymm[:2]), int(yymm[2:])
    for did in full_dids:
        # General
        did_sh = s_df[(s_df['driver-id'] == did)]
        pro_dur = sum(did_sh['productive-duration']) * SEC
        did_wt = trip_df[(trip_df['did'] == did)]
        total_fare = sum(did_wt['fare'])
        if pro_dur > 0 and total_fare != 0:
            total_prod = total_fare / pro_dur
            with open('%s/%s%s.csv' % (individual_detail_dir, general_prefix, yymm), 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow([yy, mm, did, pro_dur, total_fare, total_prod])
        #
        did_ap = ap_trip_df[(ap_trip_df['did'] == did)]
        prev_in_ap_trip = did_ap[(did_ap['trip-mode'] == DInAP_PInAP)]
        prev_out_ap_trip = did_ap[(did_ap['trip-mode'] == DOutAP_PInAP)]
        #
        if len(did_ap) != 0:
            # prev in ap trip
            ap_qu, ap_dur = sum(prev_in_ap_trip['queue-time']), sum(prev_in_ap_trip['duration'])
            ap_fare = sum(prev_in_ap_trip['fare'])
            ap_op_cost, ap_eco_profit = sum(prev_in_ap_trip['op-cost']), sum(prev_in_ap_trip['economic'])
            if ap_qu + ap_dur > 0 and ap_fare != 0:
                ap_prod = ap_fare / (ap_qu + ap_dur)
                with open('%s/%s%s.csv' % (individual_detail_dir, prev_in_ap_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([yy, mm, did, ap_qu, ap_dur, ap_fare, ap_prod, ap_op_cost, ap_eco_profit])
            #
            # prev out ap trip
            ap_qu, ap_dur = sum(prev_out_ap_trip['queue-time']), sum(prev_out_ap_trip['duration'])
            ap_fare = sum(prev_out_ap_trip['fare'])
            ap_op_cost, ap_eco_profit = sum(prev_out_ap_trip['op-cost']), sum(prev_out_ap_trip['economic'])
            if ap_qu + ap_dur > 0 and ap_fare != 0:
                ap_prod = ap_fare / (ap_qu + ap_dur)
                with open('%s/%s%s.csv' % (individual_detail_dir, prev_out_ap_prefix, yymm), 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([yy, mm, did, ap_qu, ap_dur, ap_fare, ap_prod, ap_op_cost, ap_eco_profit])    
    print 'End the file; %s' % yymm
    logging_msg('End the file; %s' % yymm)

def init_csv_files(yymm):
    with open('%s/%s%s.csv' % (individual_detail_dir, general_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        headers = ['yy', 'mm', 'did', 'total-pro-dur', 'total-fare', 'total-prod']
        writer.writerow(headers)
    #
    with open('%s/%s%s.csv' % (individual_detail_dir, prev_in_ap_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        headers = ['yy', 'mm', 'did', 'ap-queue-time', 'ap-dur', 'ap-fare', 'ap-prod', 'op-cost', 'ap-eco-profit']
        writer.writerow(headers)
    #
    with open('%s/%s%s.csv' % (individual_detail_dir, prev_out_ap_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        headers = ['yy', 'mm', 'did', 'ap-queue-time', 'ap-dur', 'ap-fare', 'ap-prod', 'op-cost', 'ap-eco-profit']
        writer.writerow(headers)

if __name__ == '__main__':
    run()
    