import __init__
#
from information_boards.c_individual_analysis import ftd_ap_stat_fpath, ftd_ns_stat_fpath
from information_boards.c_individual_analysis import ftd_trips_dir, ftd_trips_prefix
from information_boards.c_individual_analysis import ftd_shift_dir, ftd_shift_prefix
from information_boards.b_aggregated_analysis import ap_ep_dir, ap_ep_prefix
from information_boards.b_aggregated_analysis import ns_ep_dir, ns_ep_prefix
from information_boards import DIn_PIn, DOut_PIn
from information_boards import SEC60
#
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file
#
import csv
import pandas as pd


def run():
    for stat_fpath, loc, ep_dir, ep_prefix in [(ftd_ap_stat_fpath, 'ap', ap_ep_dir, ap_ep_prefix),
                                               (ftd_ns_stat_fpath, 'ns', ns_ep_dir, ns_ep_prefix),]:
        #
        with open(stat_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            headers = ['yy', 'mm', 'did'
                       'all-num', 'all-dur', 'all-fare',
                       '%s-num' % loc, '%s-dur' % loc, '%s-fare' % loc, '%s-ep' % loc, '%s-queueing-time' % loc,
                       '%sIn-num' % loc, '%sIn-dur' % loc, '%sIn-fare' % loc, '%sIn-ep' % loc, '%sIn-queueing-time' % loc,
                       '%sOut-num' % loc, '%sOut-dur' % loc, '%sOut-fare' % loc, '%sOut-ep' % loc, '%sOut-queueing-time' % loc]
            writer.writerow(headers)
        #
        for y in xrange(9, 11):
            for m in xrange(1, 13):
                yymm = '%02d%02d' % (y, m)
                if yymm in ['0912', '1010']:
                    continue
                process_files(stat_fpath, yymm, ep_dir, ep_prefix)


def process_files(stat_fpath, yymm, ep_dir, ep_prefix):
    print 'handle the file; %s' % yymm
    #
    shift_df = pd.read_csv('%s/%s%s.csv' % (ftd_shift_dir, ftd_shift_prefix, yymm))
    all_trip_df = pd.read_csv('%s/%s%s.csv' % (ftd_trips_dir, ftd_trips_prefix, yymm))
    loc_trip_df = pd.read_csv('%s/%s%s.csv' % (ep_dir, ep_prefix, yymm))
    ft_drivers = map(int, load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm)))
    #
    yy, mm = int(yymm[:2]), int(yymm[2:])
    for did in ft_drivers:
        #
        # All
        #
        d_all_trip = all_trip_df[(all_trip_df['did'] == did)]
        d_shift = shift_df[(shift_df['did'] == did)]
        all_num = len(d_all_trip['fare'])
        pro_dur = sum(d_shift['pro-dur']) * SEC60
        all_fare = sum(d_all_trip['fare'])
        #
        # Specific location
        #
        d_loc_trip = loc_trip_df[(loc_trip_df['did'] == did)]
        loc_num = len(d_loc_trip['fare'])
        loc_dur = sum(d_loc_trip['duration'])
        loc_fare = sum(d_loc_trip['fare'])
        loc_ep = sum(d_loc_trip['economic-profit'])
        loc_qtime = sum(d_loc_trip['queueing-time'])
        #
        d_loc_trip_in = d_loc_trip[(d_loc_trip['trip-mode'] == DIn_PIn)]
        locIn_num = len(d_loc_trip_in['fare'])
        locIn_dur = sum(d_loc_trip_in['duration'])
        locIn_fare = sum(d_loc_trip_in['fare'])
        locIn_ep = sum(d_loc_trip_in['economic-profit'])
        locIn_qtime = sum(d_loc_trip_in['queueing-time'])
        #
        d_loc_trip_out = d_loc_trip[(d_loc_trip['trip-mode'] == DOut_PIn)]
        locOut_num = len(d_loc_trip_out['fare'])
        locOut_dur = sum(d_loc_trip_out['duration'])
        locOut_fare = sum(d_loc_trip_out['fare'])
        locOut_ep = sum(d_loc_trip_out['economic-profit'])
        locOut_qtime = sum(d_loc_trip_out['queueing-time'])
        #
        with open(stat_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([yy, mm, did,
                             all_num, pro_dur, all_fare,
                             loc_num, loc_dur, loc_fare, loc_fare, loc_ep, loc_qtime,
                             locIn_num, locIn_dur, locIn_fare, locIn_fare, locIn_ep, locIn_qtime,
                             locOut_num, locOut_dur, locOut_fare, locOut_fare, locOut_ep, locOut_qtime])


if __name__ == '__main__':
    run()
