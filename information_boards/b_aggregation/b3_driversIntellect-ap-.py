import __init__
#
'''

'''
#
from information_boards import statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix
from information_boards import statisticsAllDriversIntellect_ap_prefix
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file, load_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import numpy as np
import statsmodels.api as sm
import csv

logger = get_logger()

sig_level = 0.01


def run():
    check_dir_create(statisticsAllDrivers_ap_dpath)
    #
    # find_intelligentDrivers()
    #
    gen_summary()


def gen_summary():
    driverIntellect2009 = load_pickle_file(
        '%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, '2009'))
    driverIntellect2010 = load_pickle_file(
        '%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, '2010'))
    driverSet2009, driverSet2010 = set(driverIntellect2009.keys()), set(driverIntellect2010.keys())
    driverSetBoth = driverSet2009.intersection(driverSet2010)
    onlySet2009 = driverSet2009.difference(driverSetBoth)
    onlySet2010 = driverSet2010.difference(driverSetBoth)
    fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, 'all')
    # fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, 'all-negativeOnly')
    with open(fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['did', 'numY2009', 'numY2010', 'coefY2009', 'coefY2010', 'coefDiff']
        writer.writerow(header)
        for did in driverSetBoth:
            num2009, coef2009 = driverIntellect2009[did]
            num2010, coef2010 = driverIntellect2010[did]
            writer.writerow([did, num2009, num2010, coef2009, coef2010, coef2009 - coef2010])
            # if coef2009 < 0 and coef2010 < 0:
            #     writer.writerow([did, num2009, num2010, coef2009, coef2010, coef2009 - coef2010])
        for did in onlySet2009:
            num2009, coef2009 = driverIntellect2009[did]
            writer.writerow([did, num2009, 0, coef2009, 0, 'X'])
        for did in onlySet2010:
            num2010, coef2010 = driverIntellect2010[did]
            writer.writerow([did, 0, num2010, 0, coef2010, 'X'])


def find_intelligentDrivers():
    for y in range(9, 11):
        year = '20%02d' % y
        dc_fpath = '%s/%s%s.pkl' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversIntellect_ap_prefix, year)
        trip_fpath = '%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix, year)
        df = pd.read_csv(trip_fpath)
        drivers = set(df['driverID'])
        intelDrivers = {}
        for did in drivers:
            did_df = df[(df['driverID'] == did)].copy(deep=True)
            months = set(did_df['month'])
            dummies = []
            for m in months:
                month_str = 'M%02d' % m
                did_df[month_str] = np.where(did_df['month'] == m, 1, 0)
                dummies.append(month_str)
            y = did_df['locQTime']
            X = did_df[dummies[:-1] + ['locIn']]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            if res.pvalues['locIn'] < sig_level:
                intelDrivers[did] = (len(did_df), res.params['locIn'])
        save_pickle_file(dc_fpath, intelDrivers)


if __name__ == '__main__':
    run()
