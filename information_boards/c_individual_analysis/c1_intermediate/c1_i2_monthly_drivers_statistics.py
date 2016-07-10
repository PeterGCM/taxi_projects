import __init__
#
from information_boards.__init__ import DIn_PIn, DOut_PIn
from information_boards.__init__ import SEC60
from b_aggregated_analysis.__init__ import ap_ep_dir, ap_ep_prefix
from b_aggregated_analysis.__init__ import ns_ep_dir, ns_ep_prefix
from c_individual_analysis.__init__ import ftd_trips_dir, ftd_trips_prefix
from c_individual_analysis.__init__ import ftd_shift_dir, ftd_shift_prefix
from c_individual_analysis.__init__ import ftd_list_dir, ftd_list_prefix
from c_individual_analysis.__init__ import ftd_stat_ap_trip_dir, ftd_stat_ap_trip_prefix
from c_individual_analysis.__init__ import ftd_stat_ns_trip_dir, ftd_stat_ns_trip_prefix
#
from taxi_common.file_handling_functions import load_pickle_file, remove_create_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import pandas as pd


def run():
    for dn in [ftd_stat_ap_trip_dir, ftd_stat_ns_trip_dir]:
        remove_create_dir(dn)
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
    for ftd_stat_dir, ftd_stat_prefix in [(ftd_stat_ap_trip_dir, ftd_stat_ap_trip_prefix),
                                          (ftd_stat_ns_trip_dir, ftd_stat_ns_trip_prefix)]:
        with open('%s/%s%s.csv' % (ftd_stat_dir, ftd_stat_prefix, yymm), 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            headers = ['yy', 'mm', 'did', 'fare', 'pro-dur', 'gen-prod'
                                        , 'pin-fare', 'pin-dur', 'pin-qu', 'pin-prod', 'pin-eco-profit'
                                        , 'pout-fare', 'pout-dur', 'pout-qu', 'pout-prod', 'pout-eco-profit']
            writer.writerow(headers)
    #
    full_dids = sorted(load_pickle_file('%s/%s%s.pkl' % (ftd_list_dir, ftd_list_prefix, yymm)))
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
        fare = sum(did_wt['fare'])
        if pro_dur > 0 and fare != 0:
            gen_prod = fare / float(pro_dur)
        else:
            continue
        for loc_trip_df, ftd_stat_dir, ftd_stat_prefix in [(ap_trip_df, ftd_stat_ap_trip_dir, ftd_stat_ap_trip_prefix),
                                                           (ns_trip_df, ftd_stat_ns_trip_dir, ftd_stat_ns_trip_prefix)]:
            did_df = loc_trip_df[(loc_trip_df['did'] == did)]
            #
            pin_trip_df = did_df[(did_df['trip-mode'] == DIn_PIn)]
            if len(pin_trip_df) == 0: continue
            pin_fare, pin_dur, pin_qu, pin_prod, pin_eco_profit = calc_prod_eco_profit(pin_trip_df)
            #
            pout_trip_df = did_df[(did_df['trip-mode'] == DOut_PIn)]
            if len(pout_trip_df) == 0: continue
            pout_fare, pout_dur, pout_qu, pout_prod, pout_eco_profit = calc_prod_eco_profit(pout_trip_df)
            #
            with open('%s/%s%s.csv' % (ftd_stat_dir, ftd_stat_prefix, yymm), 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow([yy, mm, did, fare, pro_dur, gen_prod
                                            , pin_fare, pin_dur, pin_qu, pin_prod, pin_eco_profit
                                            , pout_fare, pout_dur, pout_qu, pout_prod, pout_eco_profit])


def calc_prod_eco_profit(df):
    dur, qu = sum(df['duration']), sum(df['queueing-time'])
    fare = sum(df['fare'])
    if qu + dur > 0 and fare != 0:
        prod = fare / float(qu + dur)
    else:
        prod = 0
    eco_profit = sum(df['economic-profit'])
    return fare, dur, qu, prod, eco_profit


if __name__ == '__main__':
    run()
