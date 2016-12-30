import __init__
#
'''

'''
#
from information_boards import ssDriverTrip_dpath, ssDriverTrip_prefix
from information_boards import ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix
from information_boards import ssDriverEP_ap_dpath, ssDriverEP_ap_prefix
from information_boards import ssDriversStatisticsDayBased_ap_fpath
from information_boards import DIn_PIn, DOut_PIn
from information_boards import SEC60
#
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file
#
import pandas as pd
import csv


def run():
    with open(ssDriversStatisticsDayBased_ap_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        headers = ['year', 'month', 'day',
                   'did',
                   'allNum', 'allDur', 'allFare',
                   'apNum', 'apDur', 'apFare', 'apEP', 'apQueueingTime',
                   'apInNum', 'apInDur', 'apInFare', 'apInEP', 'apInQueueingTime',
                   'apOutNum', 'apOutDur', 'apOutFare', 'apOutEP', 'apOutQueueingTime']
        writer.writerow(headers)
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
    shift_df = pd.read_csv('%s/%s%s.csv' % (ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix, yymm))
    all_trip_df = pd.read_csv('%s/%s%s.csv' % (ssDriverTrip_dpath, ssDriverTrip_prefix, yymm))
    EP_df = pd.read_csv('%s/%s%s.csv' % (ssDriverEP_ap_dpath, ssDriverEP_ap_prefix, yymm))
    ssDrivers = map(int, load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm)))
    days = set(EP_df['day'])
    #
    yy, mm = int(yymm[:2]), int(yymm[2:])
    for dd in days:
        day_all_trip_df = all_trip_df[(all_trip_df['day'] == dd)]
        day_loc_trip_df = EP_df[(EP_df['day'] == dd)]
        day_shift_df = shift_df[(shift_df['day'] == dd)]
        for did in ssDrivers:
            #
            # All
            #
            d_all_trip = day_all_trip_df[(day_all_trip_df['did'] == did)]
            d_shift = day_shift_df[(day_shift_df['did'] == did)]
            all_num = len(d_all_trip['fare'])
            pro_dur = sum(d_shift['pro-dur']) * SEC60
            all_fare = sum(d_all_trip['fare'])
            #
            # Specific location
            #
            d_loc_trip = day_loc_trip_df[(day_loc_trip_df['did'] == did)]
            loc_num = len(d_loc_trip['fare'])
            loc_dur = sum(d_loc_trip['duration'])
            loc_fare = sum(d_loc_trip['fare'])
            loc_ep = sum(d_loc_trip['economicProfit'])
            loc_qtime = sum(d_loc_trip['queueingTime'])
            #
            d_loc_trip_in = d_loc_trip[(d_loc_trip['tripMode'] == DIn_PIn)]
            locIn_num = len(d_loc_trip_in['fare'])
            locIn_dur = sum(d_loc_trip_in['duration'])
            locIn_fare = sum(d_loc_trip_in['fare'])
            locIn_ep = sum(d_loc_trip_in['economicProfit'])
            locIn_qtime = sum(d_loc_trip_in['queueingTime'])
            #
            d_loc_trip_out = d_loc_trip[(d_loc_trip['tripMode'] == DOut_PIn)]
            locOut_num = len(d_loc_trip_out['fare'])
            locOut_dur = sum(d_loc_trip_out['duration'])
            locOut_fare = sum(d_loc_trip_out['fare'])
            locOut_ep = sum(d_loc_trip_out['economicProfit'])
            locOut_qtime = sum(d_loc_trip_out['queueingTime'])
            #
            with open(ssDriversStatisticsDayBased_ap_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([yy, mm, dd, did,
                                 all_num, pro_dur, all_fare,
                                 loc_num, loc_dur, loc_fare, loc_ep, loc_qtime,
                                 locIn_num, locIn_dur, locIn_fare, locIn_ep, locIn_qtime,
                                 locOut_num, locOut_dur, locOut_fare, locOut_ep, locOut_qtime])


if __name__ == '__main__':
    run()
