import __init__
#
'''

'''
#
from information_boards import statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix
from information_boards import statisticsAllDriversIntellect_ap_prefix
from information_boards import statisticsAllDriversDay_ap_prefix
from information_boards import SEC60
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file, load_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import numpy as np
import statsmodels.api as sm
import csv

logger = get_logger()

sig_level = 0.05
min_df_residual_ratio = 0.2

def run():
    check_dir_create(statisticsAllDrivers_ap_dpath)
    #
    # find_intelligentDrivers()

    # gen_summary()
    #
    # gen_summary2010()

    only_1001()


def only_1001():
    yymm = '1001'
    id_fpath = '%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, yymm)
    trip_fpath = '%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix, '2010')
    df = pd.read_csv(trip_fpath)
    drivers = set(df['driverID'])
    intelDrivers = {}
    for did in drivers:
        didm_df = df[(df['driverID'] == did) & (df['month'] == 1)].copy(deep=True)
        hours = set(didm_df['hour'])
        dummiesH = []
        for h in hours:
            hour_str = 'H%02d' % h
            didm_df[hour_str] = np.where(didm_df['hour'] == h, 1, 0)
            dummiesH.append(hour_str)
        df_residual = len(didm_df) - (len(dummiesH) + 1)
        if df_residual / float(len(didm_df)) < min_df_residual_ratio:
            intelDrivers[did] = (len(didm_df), 'X')
            continue
        y = didm_df['locQTime']
        X = didm_df[dummiesH[:-1] + ['locIn']]
        X = sm.add_constant(X)
        res = sm.OLS(y, X, missing='drop').fit()
        if res.pvalues['locIn'] < sig_level:
            intelDrivers[did] = (len(didm_df), res.params['locIn'])
        else:
            intelDrivers[did] = (len(didm_df), 'X')
    save_pickle_file(id_fpath, intelDrivers)


def gen_summary2010():
    intellect2010_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, '2010')
    with open(intellect2010_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['driverID', 'locInCoef',
                  'wleTripNumber', 'wleOperatingHour', 'wleFare', 
                  'locTripNumber', 'locInNumber', 'locOutNumber', 'locQTime', 'locEP', 'locDuration', 'locFare',
                  'wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity', 'locInRatio']
        writer.writerow(header)
    #
    driverIntellect2010 = load_pickle_file('%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, '2010'))
    df = pd.read_csv('%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversDay_ap_prefix, '2010'))
    agg_df = df.groupby(['driverID']).sum().reset_index()
    candi_drop_cn = []
    for cn in agg_df.columns:
        if cn not in ['driverID', 'wleTripNumber', 'wleOperatingHour', 'wleFare', 
                      'locTripNumber', 'locInNumber', 'locOutNumber', 'locQTime', 'locEP', 'locDuration', 'locFare']:
            candi_drop_cn.append(cn)
    agg_df = agg_df.drop(candi_drop_cn, axis=1)
    #
    agg_df['wleProductivity'] = agg_df['wleFare'] / agg_df['wleOperatingHour']
    agg_df['QTime/locTrip'] = agg_df['locQTime'] / agg_df['locTripNumber']
    agg_df['EP/locTrip'] = agg_df['locEP'] / agg_df['locTripNumber']
    agg_df['locProductivity'] = agg_df['locFare'] / (agg_df['locQTime'] + agg_df['locDuration']) * SEC60
    agg_df['locInRatio'] = agg_df['locInNumber'] / agg_df['locTripNumber']
    allDrivers = set(agg_df['driverID'])
    for did, (_, coef) in driverIntellect2010.iteritems():
        if coef == 'X':
            continue
        if did not in allDrivers:
            continue
        with open(intellect2010_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [did, coef]

            for cn in ['wleTripNumber', 'wleOperatingHour', 'wleFare', 
                          'locTripNumber', 'locInNumber', 'locOutNumber', 'locQTime', 'locEP', 'locDuration', 'locFare',
                          'wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity', 'locInRatio']:
                new_row += agg_df.loc[agg_df['driverID'] == did][cn].tolist()
            writer.writerow(new_row)


def gen_summary():
    driverIntellect2009 = load_pickle_file(
        '%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, '2009'))
    driverIntellect2010 = load_pickle_file(
        '%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, '2010'))
    driverSet2009, driverSet2010 = set(driverIntellect2009.keys()), set(driverIntellect2010.keys())
    driverSetBoth = driverSet2009.intersection(driverSet2010)
    onlySet2009 = driverSet2009.difference(driverSetBoth)
    onlySet2010 = driverSet2010.difference(driverSetBoth)
    # fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, 'all')
    fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, 'all-negativeOnly')
    with open(fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['did', 'numY2009', 'numY2010', 'coefY2009', 'coefY2010', 'coefDiff']
        writer.writerow(header)
        for did in driverSetBoth:
            num2009, coef2009 = driverIntellect2009[did]
            num2010, coef2010 = driverIntellect2010[did]
            # if coef2009 == 'X' or coef2010 == 'X':
            #     writer.writerow([did, num2009, num2010, coef2009, coef2010, 'X'])
            # else:
            #     writer.writerow([did, num2009, num2010, coef2009, coef2010, coef2009 - coef2010])
            if coef2009 == 'X' or coef2010 == 'X':
                continue
            if coef2009 < 0 and coef2010 < 0:
                writer.writerow([did, num2009, num2010, coef2009, coef2010, coef2009 - coef2010])
        # for did in onlySet2009:
        #     num2009, coef2009 = driverIntellect2009[did]
        #     writer.writerow([did, num2009, 0, coef2009, 0, 'X'])
        # for did in onlySet2010:
        #     num2010, coef2010 = driverIntellect2010[did]
        #     writer.writerow([did, 0, num2010, 0, coef2010, 'X'])


def find_intelligentDrivers():
    idb_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, 'both')
    with open(idb_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['', 'Y2009', 'Y2010',
                  'significance level %.2f' % sig_level, 'minDfResidualRatio %.2f' % min_df_residual_ratio]
        writer.writerow(header)
    regressionClassification = {}
    for y in range(9, 11):
        year = '20%02d' % y
        id_fpath = '%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, year)
        trip_fpath = '%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix, year)
        df = pd.read_csv(trip_fpath)
        drivers = set(df['driverID'])
        intelDrivers = {}
        for mes in ['smallObs', 'sigPos', 'sigNeg', 'XsigPos', 'XsigNeg']:
            regressionClassification[year, mes] = 0
        for did in drivers:
            did_df = df[(df['driverID'] == did)].copy(deep=True)
            months = set(did_df['month'])
            hours = set(did_df['hour'])
            dummiesM = []
            for m in months:
                month_str = 'M%02d' % m
                did_df[month_str] = np.where(did_df['month'] == m, 1, 0)
                dummiesM.append(month_str)
            dummiesH = []
            for h in hours:
                hour_str = 'H%02d' % h
                did_df[hour_str] = np.where(did_df['hour'] == h, 1, 0)
                dummiesH.append(hour_str)
            df_residual = len(did_df) - (len(dummiesM) + len(dummiesH) + 1)
            if df_residual / float(len(did_df)) < min_df_residual_ratio:
                intelDrivers[did] = (len(did_df), 'X')
                regressionClassification[year, 'smallObs'] += 1
                continue
            y = did_df['locQTime']
            X = did_df[dummiesM[:-1] + dummiesH[:-1] + ['locIn']]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            if res.pvalues['locIn'] < sig_level:
                intelDrivers[did] = (len(did_df), res.params['locIn'])
                if res.params['locIn'] > 0:
                    regressionClassification[year, 'sigPos'] += 1
                else:
                    regressionClassification[year, 'sigNeg'] += 1
            else:
                intelDrivers[did] = (len(did_df), 'X')
                if res.params['locIn'] > 0:
                    regressionClassification[year, 'XsigPos'] += 1
                else:
                    regressionClassification[year, 'XsigNeg'] += 1
        save_pickle_file(id_fpath, intelDrivers)
    #
    with open(idb_fpath, 'a') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        for mes in ['smallObs', 'sigPos', 'sigNeg', 'XsigPos', 'XsigNeg']:
            new_row = [mes, regressionClassification['2009', mes], regressionClassification['2010', mes]]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()
