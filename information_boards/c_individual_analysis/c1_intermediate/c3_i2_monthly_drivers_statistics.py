import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import DIn_PIn, DOut_PIn
from __init__ import SEC60
from b_aggregated_analysis.__init__ import ap_ep_dir, ap_ep_prefix
from b_aggregated_analysis.__init__ import ns_ep_dir, ns_ep_prefix
from c_individual_analysis.__init__ import ftd_trips_dir, ftd_trips_prefix
from c_individual_analysis.__init__ import ftd_shift_dir, ftd_shift_prefix
from c_individual_analysis.__init__ import ftd_list_dir, ftd_list_prefix
from c_individual_analysis.__init__ import ftd_gen_stat_dir, ftd_gen_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix
from c_individual_analysis.__init__ import ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix
#
from taxi_common.file_handling_functions import load_picle_file, remove_creat_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import pandas as pd
#
def run():
    for dn in [ftd_gen_stat_dir,
               ftd_prev_in_ap_stat_dir, ftd_prev_out_ap_stat_dir, 
               ftd_prev_in_ns_stat_dir, ftd_prev_out_ns_stat_dir]:
        remove_creat_dir(dn)
    #
    init_multiprocessor()
    count_num_jobs = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
#             process_files(yymm)
            put_task(process_files, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    
def process_files(yymm):
    print 'handle the file; %s' % yymm
    #
    # initialize csv_files
    #
    # general productivities
    with open('%s/%s%s.csv' % (ftd_gen_stat_dir, ftd_gen_stat_prefix, yymm), 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        headers = ['yy', 'mm', 'did', 'prod']
        writer.writerow(headers)
    # airport and night safari productivities
    for dn, fn_prefix in [(ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix),
                          (ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix),
                          (ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix),
                          (ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix)]:
        with open('%s/%s%s.csv' % (dn, fn_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            headers = ['yy', 'mm', 'did', 'prod', 'eco-profit']
            writer.writerow(headers)
    #
    full_dids = sorted(load_picle_file('%s/%s%s.pkl' % (ftd_list_dir, ftd_list_prefix, yymm)))
    s_df = pd.read_csv('%s/%s%s.csv' % (ftd_shift_dir, ftd_shift_prefix, yymm))
    trip_df = pd.read_csv('%s/%s%s.csv' % (ftd_trips_dir, ftd_trips_prefix, yymm))
    ap_trip_df = pd.read_csv('%s/%s%s.csv' % (ap_ep_dir, ap_ep_prefix, yymm))
    ns_trip_df = pd.read_csv('%s/%s%s.csv' % (ns_ep_dir, ns_ep_prefix, yymm))
    #
    yy, mm = int(yymm[:2]), int(yymm[2:])
    for did in full_dids:
        #
        # General
        #
        did_sh = s_df[(s_df['did'] == did)]
        pro_dur = sum(did_sh['pro-dur']) * SEC60
        did_wt = trip_df[(trip_df['did'] == did)]
        total_fare = sum(did_wt['fare'])
        if pro_dur > 0 and total_fare != 0:
            total_prod = total_fare / pro_dur
            with open('%s/%s%s.csv' % (ftd_gen_stat_dir, ftd_gen_stat_prefix, yymm), 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow([yy, mm, did, total_prod])
        #
        # airport trips
        #
        did_ap = ap_trip_df[(ap_trip_df['did'] == did)]
        prev_in_ap_trip = did_ap[(did_ap['trip-mode'] == DIn_PIn)]
        prev_out_ap_trip = did_ap[(did_ap['trip-mode'] == DOut_PIn)]
        #
        if len(did_ap) != 0:
            df_dir_path_prefix = [(prev_in_ap_trip, ftd_prev_in_ap_stat_dir, ftd_prev_in_ap_stat_prefix),
                                  (prev_out_ap_trip, ftd_prev_out_ap_stat_dir, ftd_prev_out_ap_stat_prefix)]
            calc_drivers_monthly_eco_profit(yymm, yy, mm, did, df_dir_path_prefix)
        #
        # night safari trips
        #
        did_ns = ns_trip_df[(ns_trip_df['did'] == did)]
        prev_in_ns_trip = did_ns[(did_ns['trip-mode'] == DIn_PIn)]
        prev_out_ns_trip = did_ns[(did_ns['trip-mode'] == DOut_PIn)]
        #
        if len(did_ns) != 0:
            df_dir_path_prefix = [(prev_in_ns_trip, ftd_prev_in_ns_stat_dir, ftd_prev_in_ns_stat_prefix),
                                  (prev_out_ns_trip, ftd_prev_out_ns_stat_dir, ftd_prev_out_ns_stat_prefix)]
            calc_drivers_monthly_eco_profit(yymm, yy, mm, did, df_dir_path_prefix)
    print 'End the file; %s' % yymm

def calc_drivers_monthly_eco_profit(yymm, yy, mm, did, df_dir_path_prefix):
    for df, dir_path, fn_prefix in df_dir_path_prefix:
        qu, dur = sum(df['queueing-time']), sum(df['duration'])
        fare = sum(df['fare'])
        eco_profit = sum(df['economic-profit'])
        if qu + dur > 0 and fare != 0:
            prod = fare / (qu + dur)
            with open('%s/%s%s.csv' % (dir_path, fn_prefix, yymm), 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow([yy, mm, did, prod, eco_profit])

if __name__ == '__main__':
    run()
