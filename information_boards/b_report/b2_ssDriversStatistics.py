import __init__
#
'''

'''
#
from information_boards import ssDriverTrip_dpath, ssDriverTrip_prefix
from information_boards import ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix
from information_boards import ssDriverEP_ap_dpath, ssDriverEP_ap_prefix
from information_boards import ssDriversStatistics_ap_fpath
from information_boards import ssDriversStatisticsDayBased_ap_fpath
from information_boards import ssDriversStatisticsMonthBased2009_ap_fpath
from information_boards import ssDriversStatisticsMonthBased2010_ap_fpath
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
    # with open(ssDriversStatisticsDayBased_ap_ori_fpath, 'wb') as w_csvfile:
    #     writer = csv.writer(w_csvfile, lineterminator='\n')
    #     headers = ['year', 'month', 'day',
    #                'did',
    #                'allNum', 'allDur', 'allFare',
    #                'apNum', 'apDur', 'apFare', 'apEP', 'apQueueingTime',
    #                'apInNum', 'apInDur', 'apInFare', 'apInEP', 'apInQueueingTime',
    #                'apOutNum', 'apOutDur', 'apOutFare', 'apOutEP', 'apOutQueueingTime']
    #     writer.writerow(headers)
    # #
    # for y in xrange(10, 11):
    #     for m in xrange(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         if yymm in ['0912', '1010']:
    #             continue
    #         process_files(yymm)
    #
    # arrange_dataAndUnits_dayBased()
    arrange_dataAndUnits_monthBased()


def arrange_dataAndUnits_tripBased():
    Y2009_df = pd.read_csv(ssDriversStatisticsMonthBased2009_ap_fpath)
    Y2010_df = pd.read_csv(ssDriversStatisticsMonthBased2010_ap_fpath)
    #
    drivers09 = set(Y2009_df['driverID'])
    drivers10 = set(Y2010_df['driverID'])
    both_year_drivers = drivers09.intersection(drivers10)
    #
    df = pd.read_csv(ssDriversStatistics_ap_fpath)

    EP_df = pd.read_csv('%s/%s%s.csv' % (ssDriverEP_ap_dpath, ssDriverEP_ap_prefix, yymm))


    df = df[(df['did'].isin(both_year_drivers))]
    # remove outlier
    fdf = df.copy(deep=True)
    fdf = fdf[(fdf['apQueueingTime'] >= SEC600)]
    for v in df.columns:
        if v in ['year', 'month', 'day', 'did']:
            continue
        fdf = fdf[~(np.abs(fdf[v] - fdf[v].mean()) > (3 * fdf[v].std()))]
    fdf = fdf[['year', 'month', 'day',
               'did',
               'allNum', 'allDur', 'allFare',
               'apNum', 'apDur', 'apFare',
               'apEP', 'apQueueingTime',
               'apInNum', 'apOutNum']]

    col_renaming_map = {
        'year': 'year', 'month': 'month', 'day': 'day',
        'did': 'driverID',
        'allNum': 'tripNumber', 'allDur': 'operatingHour', 'allFare': 'Fare',
        'apNum': 'apNumber', 'apDur': 'apDuration', 'apFare': 'apFare',
        'apEP': 'apEconomicProfit', 'apQueueingTime': 'apQTime',
        'apInNum': 'apInNumber', 'apOutNum': 'apOutNumber'
    }
    fdf = fdf.rename(columns=col_renaming_map)
    fdf['year'] = fdf['year'].apply(lambda x: x + 2000)
    fdf['operatingHour'] = fdf['operatingHour'].apply(lambda x: x / SEC3600)
    fdf['apDuration'] = fdf['apDuration'].apply(lambda x: x / SEC60)
    fdf['apQTime'] = fdf['apQTime'].apply(lambda x: x / SEC60)
    fdf['Fare'] = fdf['Fare'].apply(lambda x: x / CENT)
    fdf['apFare'] = fdf['apFare'].apply(lambda x: x / CENT)
    fdf['apEconomicProfit'] = fdf['apEconomicProfit'].apply(lambda x: x / CENT)
    #
    fdf['QTime/apTrip'] = fdf['apQTime'] / fdf['apNumber']
    fdf['economicProfit/apTrip'] = fdf['apEconomicProfit'] / fdf['apNumber']
    fdf['Productivity'] = fdf['Fare'] / fdf['operatingHour']
    fdf['apProductivity'] = fdf['apFare'] / (fdf['apDuration'] + fdf['apQTime']) * SEC60
    #
    fdf.to_csv(ssDriversStatisticsDayBased_ap_fpath, index=False)





    Y2009_df = df[(df['year'] == 2009)].copy(deep=True)
    Y2010_df = df[(df['year'] == 2010)].copy(deep=True)




def arrange_dataAndUnits_monthBased():
    df = pd.read_csv(ssDriversStatisticsDayBased_ap_fpath)
    Y2009_df = df[(df['year'] == 2009)].copy(deep=True)
    Y2010_df = df[(df['year'] == 2010)].copy(deep=True)
    months_2009 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    months_2010 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
    for Y_df, months, fpath in [(Y2009_df, months_2009, ssDriversStatisticsMonthBased2009_ap_fpath),
                                (Y2010_df, months_2010, ssDriversStatisticsMonthBased2010_ap_fpath)]:
        Y_df = Y_df.drop(['year', 'day',
                   'QTime/apTrip', 'economicProfit/apTrip', 'Productivity', 'apProductivity'], axis=1)
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
        Y_allMonths['QTime/apTrip'] = Y_allMonths['apQTime'] / Y_allMonths['apNumber']
        Y_allMonths['economicProfit/apTrip'] = Y_allMonths['apEconomicProfit'] / Y_allMonths['apNumber']
        Y_allMonths['Productivity'] = Y_allMonths['Fare'] / Y_allMonths['operatingHour']
        Y_allMonths['apProductivity'] = Y_allMonths['apFare'] / (Y_allMonths['apDuration'] + Y_allMonths['apQTime']) * 60
        Y_allMonths['apInRatio'] = Y_allMonths['apInNumber'] / Y_allMonths['apNumber']
        #
        Y_allMonths.to_csv(fpath, index=False)


def arrange_dataAndUnits_dayBased():
    df = pd.read_csv(ssDriversStatistics_ap_fpath)
    # remove outlier
    fdf = df.copy(deep=True)
    fdf = fdf[(fdf['apQueueingTime'] >= SEC600)]
    for v in df.columns:
        if v in ['year', 'month', 'day', 'did']:
            continue
        fdf = fdf[~(np.abs(fdf[v] - fdf[v].mean()) > (3 * fdf[v].std()))]
    fdf = fdf[['year', 'month', 'day',
              'did',
              'allNum', 'allDur', 'allFare',
              'apNum', 'apDur', 'apFare',
              'apEP', 'apQueueingTime',
              'apInNum', 'apOutNum']]

    col_renaming_map = {
        'year': 'year', 'month': 'month', 'day': 'day',
        'did': 'driverID',
        'allNum': 'tripNumber', 'allDur': 'operatingHour', 'allFare': 'Fare',
        'apNum': 'apNumber', 'apDur': 'apDuration', 'apFare': 'apFare',
        'apEP': 'apEconomicProfit', 'apQueueingTime': 'apQTime',
        'apInNum': 'apInNumber', 'apOutNum': 'apOutNumber'
    }
    fdf = fdf.rename(columns=col_renaming_map)
    fdf['year'] = fdf['year'].apply(lambda x: x + 2000)
    fdf['operatingHour'] = fdf['operatingHour'].apply(lambda x: x / SEC3600)
    fdf['apDuration'] = fdf['apDuration'].apply(lambda x: x / SEC60)
    fdf['apQTime'] = fdf['apQTime'].apply(lambda x: x / SEC60)
    fdf['Fare'] = fdf['Fare'].apply(lambda x: x / CENT)
    fdf['apFare'] = fdf['apFare'].apply(lambda x: x / CENT)
    fdf['apEconomicProfit'] = fdf['apEconomicProfit'].apply(lambda x: x / CENT)
    #
    fdf['QTime/apTrip'] = fdf['apQTime'] / fdf['apNumber']
    fdf['economicProfit/apTrip'] = fdf['apEconomicProfit'] / fdf['apNumber']
    fdf['Productivity'] = fdf['Fare'] / fdf['operatingHour']
    fdf['apProductivity'] = fdf['apFare'] / (fdf['apDuration'] + fdf['apQTime']) * SEC60
    #
    fdf.to_csv(ssDriversStatisticsDayBased_ap_fpath, index=False)


def process_files(yymm):
    print 'handle the file; %s' % yymm
    #
    shift_df = pd.read_csv('%s/%s%s.csv' % (ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix, yymm))
    all_trip_df = pd.read_csv('%s/%s%s.csv' % (ssDriverTrip_dpath, ssDriverTrip_prefix, yymm))
    EP_df = pd.read_csv('%s/%s%s.csv' % (ssDriverEP_ap_dpath, ssDriverEP_ap_prefix, yymm))
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
            with open(ssDriversStatistics_ap_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([yy, mm, dd, did,
                                 all_num, pro_dur, all_fare,
                                 loc_num, loc_dur, loc_fare, loc_ep, loc_qtime,
                                 locIn_num, locIn_dur, locIn_fare, locIn_ep, locIn_qtime,
                                 locOut_num, locOut_dur, locOut_fare, locOut_ep, locOut_qtime])


if __name__ == '__main__':
    run()
