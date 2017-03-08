import __init__
#
'''

'''
#
from information_boards import statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix
from information_boards import dpaths, prefixs
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
of_dpath = dpaths['individualAnalysis']
of_prefix = prefixs['individualAnalysis']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


header_base = ['driverID', 'numObs', 'dfResidual',
               'constCoef', 'constPV',
               'locInCoef', 'locInPV',
               'wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']


def run():
    locIn_Reg()
    # locIn_F_W_Reg()
    # locIn_F_H_Reg()
    # locIn_F_M_Reg()
    # locIn_F_WH_Reg()
    # locIn_F_WM_Reg()
    # locIn_F_HM_Reg()
    # locIn_F_WHM_Reg()


def locIn_F_WHM_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    wholeHours = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    wholeMonths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
    #
    ofPath = '%s/%s%s-locIn-F(WHM).csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        header += ['weekEndCoef', 'weekEndPV']
        for h in wholeHours:
            header += ['H%02dCoef' % h, 'H%02dPV' % h]
        for m in wholeMonths:
            header += ['M%02dCoef' % m, 'M%02dPV' % m]
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            didTripHours = set(didTripDF['hour'])
            dummiesH = []
            for h in didTripHours:
                hour_str = 'H%02d' % h
                didTripDF[hour_str] = np.where(didTripDF['hour'] == h, 1, 0)
                dummiesH.append(hour_str)
            didTripMonths = set(didTripDF['month'])
            dummiesM = []
            for m in didTripMonths:
                month_str = 'M%02d' % m
                didTripDF[month_str] = np.where(didTripDF['month'] == m, 1, 0)
                dummiesM.append(month_str)
            omittedDummyH = dummiesH[-1]
            omittedDummyM = dummiesM[-1]
            numObs = len(didTripDF)
            idvs = ['locIn'] + ['weekEnd'] + dummiesH[:-1] + dummiesM[:-1]
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
                new_row += [res.params['weekEnd'], res.pvalues['weekEnd']]
                for h in wholeHours:
                    hour_str = 'H%02d' % h
                    if hour_str in dummiesH:
                        if hour_str == omittedDummyH:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[hour_str], res.pvalues[hour_str]]
                    else:
                        new_row += ['X', 'X']
                for m in wholeMonths:
                    month_str = 'M%02d' % m
                    if month_str in dummiesM:
                        if month_str == omittedDummyM:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[month_str], res.pvalues[month_str]]
                    else:
                        new_row += ['X', 'X']
            writer.writerow(new_row)


def locIn_F_HM_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    wholeHours = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    wholeMonths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
    #
    ofPath = '%s/%s%s-locIn-F(HM).csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        for h in wholeHours:
            header += ['H%02dCoef' % h, 'H%02dPV' % h]
        for m in wholeMonths:
            header += ['M%02dCoef' % m, 'M%02dPV' % m]
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            didTripHours = set(didTripDF['hour'])
            dummiesH = []
            for h in didTripHours:
                hour_str = 'H%02d' % h
                didTripDF[hour_str] = np.where(didTripDF['hour'] == h, 1, 0)
                dummiesH.append(hour_str)
            didTripMonths = set(didTripDF['month'])
            dummiesM = []
            for m in didTripMonths:
                month_str = 'M%02d' % m
                didTripDF[month_str] = np.where(didTripDF['month'] == m, 1, 0)
                dummiesM.append(month_str)
            omittedDummyH = dummiesH[-1]
            omittedDummyM = dummiesM[-1]
            numObs = len(didTripDF)
            idvs = ['locIn'] + dummiesH[:-1] + dummiesM[:-1]
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
                for h in wholeHours:
                    hour_str = 'H%02d' % h
                    if hour_str in dummiesH:
                        if hour_str == omittedDummyH:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[hour_str], res.pvalues[hour_str]]
                    else:
                        new_row += ['X', 'X']
                for m in wholeMonths:
                    month_str = 'M%02d' % m
                    if month_str in dummiesM:
                        if month_str == omittedDummyM:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[month_str], res.pvalues[month_str]]
                    else:
                        new_row += ['X', 'X']
            writer.writerow(new_row)


def locIn_F_WM_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    wholeMonths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
    #
    ofPath = '%s/%s%s-locIn-F(WM).csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        header += ['weekEndCoef', 'weekEndPV']
        for m in wholeMonths:
            header += ['M%02dCoef' % m, 'M%02dPV' % m]
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            didTripMonths = set(didTripDF['month'])
            dummiesM = []
            for m in didTripMonths:
                month_str = 'M%02d' % m
                didTripDF[month_str] = np.where(didTripDF['month'] == m, 1, 0)
                dummiesM.append(month_str)
            omittedDummyM = dummiesM[-1]
            numObs = len(didTripDF)
            idvs = ['locIn'] + ['weekEnd'] + dummiesM[:-1]
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
                new_row += [res.params['weekEnd'], res.pvalues['weekEnd']]
                for m in wholeMonths:
                    month_str = 'M%02d' % m
                    if month_str in dummiesM:
                        if month_str == omittedDummyM:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[month_str], res.pvalues[month_str]]
                    else:
                        new_row += ['X', 'X']
            writer.writerow(new_row)



def locIn_F_WH_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    wholeHours = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    #
    ofPath = '%s/%s%s-locIn-F(WH).csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        header += ['weekEndCoef', 'weekEndPV']
        for h in wholeHours:
            header += ['H%02dCoef' % h, 'H%02dPV' % h]
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            didTripHours = set(didTripDF['hour'])
            dummiesH = []
            for h in didTripHours:
                hour_str = 'H%02d' % h
                didTripDF[hour_str] = np.where(didTripDF['hour'] == h, 1, 0)
                dummiesH.append(hour_str)
            omittedDummyH = dummiesH[-1]
            numObs = len(didTripDF)
            idvs = ['locIn'] + ['weekEnd'] + dummiesH[:-1]
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
                new_row += [res.params['weekEnd'], res.pvalues['weekEnd']]
                for h in wholeHours:
                    hour_str = 'H%02d' % h
                    if hour_str in dummiesH:
                        if hour_str == omittedDummyH:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[hour_str], res.pvalues[hour_str]]
                    else:
                        new_row += ['X', 'X']
            writer.writerow(new_row)


def locIn_F_M_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    wholeMonths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]
    #
    ofPath = '%s/%s%s-locIn-F(M).csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        for m in wholeMonths:
            header += ['M%02dCoef' % m, 'M%02dPV' % m]
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            didTripMonths = set(didTripDF['month'])
            dummiesM = []
            for m in didTripMonths:
                month_str = 'M%02d' % m
                didTripDF[month_str] = np.where(didTripDF['month'] == m, 1, 0)
                dummiesM.append(month_str)
            omittedDummyM = dummiesM[-1]
            numObs = len(didTripDF)
            idvs = ['locIn'] + dummiesM[:-1]
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
                for m in wholeMonths:
                    month_str = 'M%02d' % m
                    if month_str in dummiesM:
                        if month_str == omittedDummyM:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[month_str], res.pvalues[month_str]]
                    else:
                        new_row += ['X', 'X']
            writer.writerow(new_row)


def locIn_F_H_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    wholeHours = [0, 1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
    #
    ofPath = '%s/%s%s-locIn-F(H).csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        for h in wholeHours:
            header += ['H%02dCoef' % h, 'H%02dPV' % h] 
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            didTripHours = set(didTripDF['hour'])
            dummiesH = []
            for h in didTripHours:
                hour_str = 'H%02d' % h
                didTripDF[hour_str] = np.where(didTripDF['hour'] == h, 1, 0)
                dummiesH.append(hour_str)
            omittedDummyH = dummiesH[-1]
            numObs = len(didTripDF)
            idvs = ['locIn'] + dummiesH[:-1]
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
                for h in wholeHours:
                    hour_str = 'H%02d' % h
                    if hour_str in dummiesH:
                        if hour_str == omittedDummyH:
                            new_row += ['-', '-']
                        else:
                            new_row += [res.params[hour_str], res.pvalues[hour_str]]
                    else:
                        new_row += ['X', 'X']
            writer.writerow(new_row)


def locIn_F_W_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    #
    ofPath = '%s/%s%s-locIn-F(W).csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        header += ['weekEndCoef', 'weekEndPV']
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            numObs = len(didTripDF)
            idvs = ['locIn'] + ['weekEnd']
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
                new_row += [res.params['weekEnd'], res.pvalues['weekEnd']]
            writer.writerow(new_row)


def locIn_Reg():
    tripDF, yearDF = data_load()
    drivers = set(tripDF['driverID'])
    #
    ofPath = '%s/%s%s-locIn-F().csv' % (of_dpath, of_prefix, '2010')
    with open(ofPath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = header_base
        writer.writerow(header)
        for did in drivers:
            didTripDF = tripDF[(tripDF['driverID'] == did)].copy(deep=True)
            numObs = len(didTripDF)
            idvs = ['locIn']
            dfResidual = numObs - (len(idvs) + 1)
            new_row = [did, numObs, dfResidual]
            if dfResidual <= 0:
                for cn in header:
                    if cn in ['driverID', 'numObs', 'dfResidual']:
                        continue
                    new_row += ['X']
            else:
                y = didTripDF['locQTime']
                X = didTripDF[idvs]
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                #
                try:
                    new_row += [res.params['const'], res.pvalues['const']]
                except KeyError:
                    new_row += ['X', 'X']
                new_row += [res.params['locIn'], res.pvalues['locIn']]
                for cn in ['wleProductivity', 'QTime/locTrip', 'EP/locTrip', 'locProductivity']:
                    new_row += yearDF.loc[yearDF['driverID'] == did][cn].tolist()
            writer.writerow(new_row)


def data_load():
    tripDF = pd.read_csv(
        '%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix, '2010'))
    dayDF = pd.read_csv(
        '%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversDay_ap_prefix, '2010'))
    yearDF = dayDF.groupby(['driverID']).sum().reset_index()
    drop_cns = []
    for cn in yearDF.columns:
        if cn not in ['driverID', 'wleTripNumber', 'wleOperatingHour', 'wleFare',
                      'locTripNumber', 'locInNumber', 'locOutNumber', 'locQTime', 'locEP', 'locDuration', 'locFare']:
            drop_cns.append(cn)
    yearDF = yearDF.drop(drop_cns, axis=1)
    #
    yearDF['wleProductivity'] = yearDF['wleFare'] / yearDF['wleOperatingHour']
    yearDF['QTime/locTrip'] = yearDF['locQTime'] / yearDF['locTripNumber']
    yearDF['EP/locTrip'] = yearDF['locEP'] / yearDF['locTripNumber']
    yearDF['locProductivity'] = yearDF['locFare'] / (yearDF['locQTime'] + yearDF['locDuration']) * SEC60
    yearDF = yearDF.drop(['wleTripNumber', 'wleOperatingHour', 'wleFare',
                            'locTripNumber', 'locInNumber', 'locOutNumber',
                          'locQTime', 'locEP', 'locDuration', 'locFare'], axis=1)
    return tripDF, yearDF


if __name__ == '__main__':
    run()
