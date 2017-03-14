import __init__
#
'''

'''
#
from information_boards import ssDriverTrip_dpath, ssDriverTrip_prefix
from information_boards import ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix
from information_boards import ssDriverEP_ns_dpath, ssDriverEP_ns_prefix
from information_boards import ssDriversStatistics_ns1519_fpath
from information_boards import ssDriversStatistics_ns2000_fpath
from information_boards import ssDriversStatisticsDayBasedModi_ns1519_fpath
from information_boards import ssDriversStatisticsDayBasedModi_ns2000_fpath
from information_boards import ssDriversStatisticsMonthBased2009_ns1519_fpath
from information_boards import ssDriversStatisticsMonthBased2009_ns2000_fpath
from information_boards import ssDriversStatisticsMonthBased2010_ns1519_fpath
from information_boards import ssDriversStatisticsMonthBased2010_ns2000_fpath


# from information_boards import ssDriverEP_ap_all_fpath
# from information_boards import ssDriversStatistics_ap_fpath
# from information_boards import ssDriversStatisticsDayBasedModi_ap_fpath
# from information_boards import ssDriversStatisticsMonthBased2009_ap_fpath
# from information_boards import ssDriversStatisticsMonthBased2010_ap_fpath
# from information_boards import ssDriversStatisticsTripBased2009_ap_fpath
# from information_boards import ssDriversStatisticsTripBased2010_ap_fpath
from information_boards import DIn_PIn, DOut_PIn
from information_boards import SEC3600, SEC600, SEC60, CENT
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file
#
import pandas as pd
import numpy as np
import csv


def run():
    # for ofpath in [ssDriversStatistics_ns1519_fpath, ssDriversStatistics_ns2000_fpath]:
    #     with open(ofpath, 'wb') as w_csvfile:
    #         writer = csv.writer(w_csvfile, lineterminator='\n')
    #         headers = ['year', 'month', 'day',
    #                    'did',
    #                    'allNum', 'allDur', 'allFare',
    #                    'nsNum', 'nsDur', 'nsFare', 'nsEP', 'nsQueueingTime',
    #                    'nsInNum', 'nsInDur', 'nsInFare', 'nsInEP', 'nsInQueueingTime',
    #                    'nsOutNum', 'nsOutDur', 'nsOutFare', 'nsOutEP', 'nsOutQueueingTime']
    #         writer.writerow(headers)
    # #
    # for y in xrange(9, 11):
    #     for m in xrange(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         if yymm in ['0912', '1010']:
    #             continue
    #         aggregate_dayBased(yymm)
    #
    # arrange_dataAndUnits_dayBased()
    arrange_dataAndUnits_monthBased()
    # arrange_dataAndUnits_tripBased()

def arrange_dataAndUnits_monthBased():
    for modi_fpath, monthBased2009_fpath, monthBased2010_fpath in [(ssDriversStatisticsDayBasedModi_ns1519_fpath,
                                                                      ssDriversStatisticsMonthBased2009_ns1519_fpath,
                                                                      ssDriversStatisticsMonthBased2010_ns1519_fpath),
                                                                   (ssDriversStatisticsDayBasedModi_ns2000_fpath,
                                                                    ssDriversStatisticsMonthBased2009_ns2000_fpath,
                                                                    ssDriversStatisticsMonthBased2010_ns2000_fpath)]:
        df = pd.read_csv(modi_fpath)
        Y2009_df = df[(df['year'] == 2009)].copy(deep=True)
        Y2010_df = df[(df['year'] == 2010)].copy(deep=True)
        months_2009 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        months_2010 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
        for Y_df, months, fpath in [(Y2009_df, months_2009, monthBased2009_fpath),
                                    (Y2010_df, months_2010, monthBased2010_fpath)]:
            Y_df = Y_df.drop(['year', 'day',
                       'QTime/nsTrip', 'economicProfit/nsTrip', 'Productivity', 'nsProductivity'], axis=1)
            monthBased_df = Y_df.groupby(['month', 'driverID']).sum().reset_index()
            drivers = {}
            for m in months:
                for did in monthBased_df[(monthBased_df['month'] == m)]['driverID']:
                    if not drivers.has_key(did):
                        drivers[did] = 0
                    drivers[did] += 1
            # filtering
            all_month_drivers = [k for k, v in drivers.iteritems() if v == len(months)]
            Y_allMonths = monthBased_df[(monthBased_df['driverID'].isin(all_month_drivers))]
            #
            Y_allMonths['month^2'] = Y_allMonths['month'].apply(lambda x: x ** 2)
            Y_allMonths['QTime/nsTrip'] = Y_allMonths['nsQTime'] / Y_allMonths['nsNumber']
            Y_allMonths['economicProfit/nsTrip'] = Y_allMonths['nsEconomicProfit'] / Y_allMonths['nsNumber']
            Y_allMonths['Productivity'] = Y_allMonths['Fare'] / Y_allMonths['operatingHour']
            Y_allMonths['nsProductivity'] = Y_allMonths['nsFare'] / (Y_allMonths['nsDuration'] + Y_allMonths['nsQTime']) * 60
            Y_allMonths['nsInRatio'] = Y_allMonths['nsInNumber'] / Y_allMonths['nsNumber']
            #
            Y_allMonths.to_csv(fpath, index=False)


def arrange_dataAndUnits_dayBased():
    for ori_fpath, modi_fpath in [(ssDriversStatistics_ns1519_fpath, ssDriversStatisticsDayBasedModi_ns1519_fpath),
                                  (ssDriversStatistics_ns2000_fpath, ssDriversStatisticsDayBasedModi_ns2000_fpath)]:
        df = pd.read_csv(ori_fpath)
        # remove outlier
        fdf = df.copy(deep=True)
        fdf = fdf[(fdf['nsQueueingTime'] >= SEC600)]
        for v in df.columns:
            if v in ['year', 'month', 'day', 'did']:
                continue
            fdf = fdf[~(np.abs(fdf[v] - fdf[v].mean()) > (3 * fdf[v].std()))]
        fdf = fdf[['year', 'month', 'day',
                  'did',
                  'allNum', 'allDur', 'allFare',
                  'nsNum', 'nsDur', 'nsFare',
                  'nsEP', 'nsQueueingTime',
                  'nsInNum', 'nsOutNum']]

        col_renaming_map = {
            'year': 'year', 'month': 'month', 'day': 'day',
            'did': 'driverID',
            'allNum': 'tripNumber', 'allDur': 'operatingHour', 'allFare': 'Fare',
            'nsNum': 'nsNumber', 'nsDur': 'nsDuration', 'nsFare': 'nsFare',
            'nsEP': 'nsEconomicProfit', 'nsQueueingTime': 'nsQTime',
            'nsInNum': 'nsInNumber', 'nsOutNum': 'nsOutNumber'
        }
        fdf = fdf.rename(columns=col_renaming_map)
        fdf['year'] = fdf['year'].apply(lambda x: x + 2000)
        fdf['operatingHour'] = fdf['operatingHour'].apply(lambda x: x / SEC3600)
        fdf['nsDuration'] = fdf['nsDuration'].apply(lambda x: x / SEC60)
        fdf['nsQTime'] = fdf['nsQTime'].apply(lambda x: x / SEC60)
        fdf['Fare'] = fdf['Fare'].apply(lambda x: x / CENT)
        fdf['nsFare'] = fdf['nsFare'].apply(lambda x: x / CENT)
        fdf['nsEconomicProfit'] = fdf['nsEconomicProfit'].apply(lambda x: x / CENT)
        #
        fdf['QTime/nsTrip'] = fdf['nsQTime'] / fdf['nsNumber']
        fdf['economicProfit/nsTrip'] = fdf['nsEconomicProfit'] / fdf['nsNumber']
        fdf['Productivity'] = fdf['Fare'] / fdf['operatingHour']
        fdf['nsProductivity'] = fdf['nsFare'] / (fdf['nsDuration'] + fdf['nsQTime']) * SEC60
        #
        fdf.to_csv(modi_fpath, index=False)


def aggregate_dayBased(yymm):
    print 'handle the file; %s' % yymm
    #
    for hours, fpath in [([15, 16, 17, 18, 19], ssDriversStatistics_ns1519_fpath),
                         ([20, 21, 22, 23, 0], ssDriversStatistics_ns2000_fpath)]:
        shift_df = pd.read_csv('%s/%s%s.csv' % (ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix, yymm))
        shift_df = shift_df[shift_df['hh'].isin(hours)]
        all_trip_df = pd.read_csv('%s/%s%s.csv' % (ssDriverTrip_dpath, ssDriverTrip_prefix, yymm))
        all_trip_df = all_trip_df[all_trip_df['hour'].isin(hours)]
        EP_df = pd.read_csv('%s/%s%s.csv' % (ssDriverEP_ns_dpath, ssDriverEP_ns_prefix, yymm))
        EP_df = EP_df[EP_df['hour'].isin(hours)]
        ssDrivers = map(int, load_pickle_file('%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yymm)))
        days = set(EP_df['day'])
        #
        yy, mm = int(yymm[:2]), int(yymm[2:])
        for dd in days:
            day_all_trip_df = all_trip_df[(all_trip_df['day'] == dd)]
            day_loc_trip_df = EP_df[(EP_df['day'] == dd)]
            day_shift_df = shift_df[(shift_df['dd'] == dd)]
            for did in ssDrivers:
                #
                # Specific location
                #
                d_loc_trip = day_loc_trip_df[(day_loc_trip_df['did'] == did)]
                if len(d_loc_trip) == 0:
                    continue
                loc_num = len(d_loc_trip['fare'])
                loc_dur = sum(d_loc_trip['duration'])
                loc_fare = sum(d_loc_trip['fare'])
                loc_ep = sum(d_loc_trip['economicProfit'])
                loc_qtime = sum(d_loc_trip['queueingTime'])
                #
                # All
                #
                d_all_trip = day_all_trip_df[(day_all_trip_df['did'] == did)]
                d_shift = day_shift_df[(day_shift_df['did'] == did)]
                all_num = len(d_all_trip['fare'])
                pro_dur = sum(d_shift['pro-dur']) * SEC60
                all_fare = sum(d_all_trip['fare'])
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
                with open(fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow([yy, mm, dd, did,
                                     all_num, pro_dur, all_fare,
                                     loc_num, loc_dur, loc_fare, loc_ep, loc_qtime,
                                     locIn_num, locIn_dur, locIn_fare, locIn_ep, locIn_qtime,
                                     locOut_num, locOut_dur, locOut_fare, locOut_ep, locOut_qtime])
#
# def arrange_dataAndUnits_tripBased():
#     Y2009_df = pd.read_csv(ssDriversStatisticsMonthBased2009_ap_fpath)
#     Y2010_df = pd.read_csv(ssDriversStatisticsMonthBased2010_ap_fpath)
#     #
#     drivers09 = set(Y2009_df['driverID'])
#     drivers10 = set(Y2010_df['driverID'])
#     both_year_drivers = drivers09.intersection(drivers10)
#     #
#     df = pd.read_csv(ssDriverEP_ap_all_fpath)
#     df = df[(df['did'].isin(both_year_drivers))]
#     # remove outlier
#     fdf = df.copy(deep=True)
#     fdf = fdf[(fdf['queueingTime'] >= SEC600)]
#     for v in ['queueingTime', 'economicProfit']:
#         fdf = fdf[~(np.abs(fdf[v] - fdf[v].mean()) > (3 * fdf[v].std()))]
#     fdf['apIn'] = np.where(fdf['tripMode'] == DIn_PIn, 1, 0)
#
#     fdf = fdf[['did',
#                'duration', 'fare',
#                'apIn', 'queueingTime', 'economicProfit',
#                'year', 'month', 'day', 'hour']]
#     col_renaming_map = {'year': 'year', 'month': 'month', 'day': 'day',
#                         'did': 'driverID',
#                         'duration': 'apDuration', 'fare': 'apFare',
#                         'queueingTime': 'apQTime', 'economicProfit': 'apEconomicProfit'}
#     fdf = fdf.rename(columns=col_renaming_map)
#     fdf['month^2'] = fdf['month'].apply(lambda x: x ** 2)
#     fdf['apDuration'] = fdf['apDuration'].apply(lambda x: x / SEC60)
#     fdf['apQTime'] = fdf['apQTime'].apply(lambda x: x / SEC60)
#     fdf['apFare'] = fdf['apFare'].apply(lambda x: x / CENT)
#     fdf['apEconomicProfit'] = fdf['apEconomicProfit'].apply(lambda x: x / CENT)
#     fdf['apProductivity'] = fdf['apFare'] / (fdf['apDuration'] + fdf['apQTime']) * SEC60
#     #
#     Y2009_df = fdf[(fdf['year'] == 2009)].copy(deep=True)
#     Y2010_df = fdf[(fdf['year'] == 2010)].copy(deep=True)
#     Y2009_df.to_csv(ssDriversStatisticsTripBased2009_ap_fpath, index=False)
#     Y2010_df.to_csv(ssDriversStatisticsTripBased2010_ap_fpath, index=False)
#


if __name__ == '__main__':
    run()
