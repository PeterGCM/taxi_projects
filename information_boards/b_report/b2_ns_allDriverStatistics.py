import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import shiftProDur_dpath, shiftProDur_prefix
from information_boards import economicProfit_ns_dpath, economicProfit_ns_prefix
from information_boards import statisticsAllDrivers_ns_dpath
from information_boards import statisticsAllDriversDay_ns1517_prefix, statisticsAllDriversMonth_ns1517_prefix, statisticsAllDriversTrip_ns1517_prefix
from information_boards import statisticsAllDriversYear_ns1517_prefix
from information_boards import statisticsAllDriversDay_ns2023_prefix, statisticsAllDriversMonth_ns2023_prefix, statisticsAllDriversTrip_ns2023_prefix
from information_boards import statisticsAllDriversYear_ns2023_prefix
from information_boards import DIn_PIn, DOut_PIn
from information_boards import SEC3600, SEC600, SEC60, CENT
from information_boards import HOLIDAYS2009, HOLIDAYS2010
from information_boards import WEEKENDS
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, get_all_files
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime
import numpy as np
import pandas as pd

logger = get_logger()

WTN, WOH, WF, \
LTN, LIN, LON, \
LQ, LEP, \
LD, LF = range(10)

tf_ns1517 = [15, 16, 17]
tf_ns2023 = [20, 21, 22, 23]


def run():
    check_dir_create(statisticsAllDrivers_ns_dpath)
    #
    # process_tripBased()
    # filter_tripBased()
    #
    # process_dayBased()
    # filter_dayBased()
    #
    process_monthBased()
    #
    # for y in range(9, 11):
    #     yyyy = '20%02d' % y
    #     aggregate_monthBased(yyyy)
    #
    # aggregate_yearBased()
    # for y in range(9, 11):
    #     yyyy = '20%02d' % y
    #     process_tripbased(yyyy)


def process_tripBased():
    for y in range(9, 11):
        yyyy = '20%02d' % y
        logger.info('handle the file; %s' % yyyy)
        logger.info('handle the file; %s' % yyyy)
        #
        statistics1517_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversTrip_ns1517_prefix, yyyy)
        statistics2023_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversTrip_ns2023_prefix, yyyy)
        #
        yy = yyyy[2:]
        holidays = HOLIDAYS2009 if yyyy == '2009' else HOLIDAYS2010
        for statistics_fpath in [statistics1517_fpath, statistics2023_fpath]:
            with open(statistics_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                header = ['year', 'month', 'day', 'hour',
                          'driverID',
                          'locQTime', 'locEP', 'locDuration', 'locFare',
                          'locProductivity',
                          'locIn', 'weekEnd']
                writer.writerow(header)
        for fn in get_all_files(economicProfit_ns_dpath, '%s%s*' % (economicProfit_ns_prefix, yy)):
            with open('%s/%s' % (economicProfit_ns_dpath, fn), 'rt') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
                    did = int(row[hid['did']])
                    locQTime = float(row[hid['queueingTime']]) / SEC60
                    locEP = float(row[hid['economicProfit']]) / CENT
                    locDuration = float(row[hid['duration']]) / SEC60
                    locFare = float(row[hid['fare']]) / CENT
                    locProductivity = (locFare / (locQTime + locDuration)) * SEC60
                    locIn = 1 if int(row[hid['tripMode']]) == DIn_PIn else 0
                    weekEnd = 0
                    if (year, month, day) in holidays:
                        weekEnd = 1
                    if datetime.datetime(year, month, day).weekday() in WEEKENDS:
                        weekEnd = 1
                    if hour in tf_ns1517:
                        statistics_fpath = statistics1517_fpath
                    elif hour in tf_ns2023:
                        statistics_fpath = statistics2023_fpath
                    else:
                        continue
                    with open(statistics_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [
                            year, month, day, hour,
                            did,
                            locQTime, locEP, locDuration, locFare,
                            locProductivity,
                            locIn, weekEnd]
                        writer.writerow(new_row)


def filter_tripBased():
    for y in range(9, 11):
        yyyy = '20%02d' % y
        logger.info('handle the file; %s' % yyyy)
        for statisticsAllDriversTrip_ns_prefix in [statisticsAllDriversTrip_ns1517_prefix, statisticsAllDriversTrip_ns2023_prefix]:
            Ydf = pd.read_csv('%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversTrip_ns_prefix, yyyy))
            outlier_index = set()
            for cn in Ydf.columns:
                if cn in ['year', 'month', 'day', 'hour', 'driverID']:
                    continue
                if cn == 'locQTime':
                    outlier_set = set(np.where(Ydf[cn] > 120)[0].tolist())
                    outlier_index = outlier_index.union(set(outlier_set))
                if cn in ['locEP', 'locProductivity']:
                    outlier_set = np.where((np.abs(Ydf[cn] - Ydf[cn].mean()) > (3 * Ydf[cn].std())))[0]
                    outlier_index = outlier_index.union(set(outlier_set))
            Ydf = Ydf.drop(Ydf.index[list(outlier_index)])
            Ydf.to_csv('%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversTrip_ns_prefix, yyyy), index=False)


def process_dayBased():
    logger.info('handle dayBased')
    #
    for y in range(9, 11):
        yyyy = '20%02d' % y
        logger.info('handle the file; %s' % yyyy)
        statistics1517_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversDay_ns1517_prefix, yyyy)
        statistics2023_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversDay_ns2023_prefix, yyyy)
        #
        dateDid_statistics1517, dateDid_statistics2023 = {}, {}
        logger.info('process locTrip')
        for ns_prefix, dateDid_statistics in [(statisticsAllDriversTrip_ns1517_prefix, dateDid_statistics1517),
                                                   (statisticsAllDriversTrip_ns2023_prefix, dateDid_statistics2023)]:
            tripBased_fpath = '%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ns_dpath, ns_prefix, yyyy)
            logger.info('process locTrip')
            with open(tripBased_fpath, 'rt') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    year, month, day = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day']])
                    did = int(row[hid['driverID']])
                    k = (year, month, day, did)
                    if not dateDid_statistics.has_key(k):
                        dateDid_statistics[k] = [0.0 for _ in [WTN, WOH, WF, LTN, LIN, LON, LQ, LEP, LD, LF]]
                    dateDid_statistics[k][LTN] += 1
                    if int(row[hid['locIn']]) == 1:
                        dateDid_statistics[k][LIN] += 1
                    else:
                        assert int(row[hid['locIn']]) == 0
                        dateDid_statistics[k][LON] += 1
                    dateDid_statistics[k][LQ] += float(row[hid['locQTime']])
                    dateDid_statistics[k][LEP] += float(row[hid['locEP']])
                    dateDid_statistics[k][LD] += float(row[hid['locDuration']])
                    dateDid_statistics[k][LF] += float(row[hid['locFare']])
        yy = yyyy[2:]
        logger.info('process shift')
        for fn in get_all_files(shiftProDur_dpath, '%s%s*' % (shiftProDur_prefix, yy)):
            logger.info('shift; %s' % fn)
            with open('%s/%s' % (shiftProDur_dpath, fn), 'rt') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    year, month, day, hour = 2000 + int(row[hid['yy']]), int(row[hid['mm']]), int(row[hid['dd']]), int(row[hid['hh']])
                    if hour in tf_ns1517:
                        dateDid_statistics = dateDid_statistics1517
                    elif hour in tf_ns2023:
                        dateDid_statistics = dateDid_statistics2023
                    else:
                        continue
                    did = int(row[hid['did']])
                    k = (year, month, day, did)
                    if not dateDid_statistics.has_key(k):
                        continue
                    dateDid_statistics[k][WOH] += (float(row[hid['pro-dur']]) * SEC60) / SEC3600

        logger.info('process trip')
        for fn in get_all_files(trip_dpath, '%s%s*' % (trip_prefix, yy)):
            logger.info('Trip; %s' % fn)
            _, yymm = fn[:-len('.csv')].split('-')
            yy, mm = yymm[:2], yymm[-2:]
            year, month = 2000 + int(yy), int(mm)
            with open('%s/%s' % (trip_dpath, fn), 'rt') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    day, hour = int(row[hid['day']]), int(row[hid['hour']])
                    if hour in tf_ns1517:
                        dateDid_statistics = dateDid_statistics1517
                    elif hour in tf_ns2023:
                        dateDid_statistics = dateDid_statistics2023
                    else:
                        continue
                    did = int(row[hid['did']])
                    k = (year, month, day, did)
                    if not dateDid_statistics.has_key(k):
                        continue
                    dateDid_statistics[k][WTN] += 1
                    dateDid_statistics[k][WF] += float(row[hid['fare']]) / CENT
        #
        logger.info('write statistics; %s' % yymm)
        for statistics_fpath, dateDid_statistics in [(statistics1517_fpath, dateDid_statistics1517),
                                                     (statistics2023_fpath, dateDid_statistics2023)]:
            with open(statistics_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                header = ['year', 'month', 'day', 'driverID',
                          'wleTripNumber', 'wleOperatingHour', 'wleFare',
                          'wleProductivity',
                          'locTripNumber', 'locInNumber', 'locOutNumber',
                          'locQTime', 'locEP', 'locDuration', 'locFare',
                          'QTime/locTrip', 'EP/locTrip',
                          'locProductivity']
                writer.writerow(header)
                for (year, month, day, did), statistics in dateDid_statistics.iteritems():
                    wleTripNumber, wleOperatingHour, wleFare = int(statistics[WTN]), statistics[WOH], statistics[WF],
                    if wleOperatingHour == 0.0:
                        continue
                    wleProductivity = wleFare / wleOperatingHour
                    #
                    locTripNumber, locInNumber, locOutNumber = map(int, [statistics[LTN], statistics[LIN], statistics[LON]])
                    if locTripNumber == 0.0:
                        continue
                    locQTime, locEP, locDuration, locFare = statistics[LQ], statistics[LEP], statistics[LD], statistics[LF]
                    if (locQTime + locDuration) == 0.0:
                        continue
                    QTime_locTrip, EP_locTrip = locQTime / float(locTripNumber), locEP / float(locTripNumber)
                    locProductivity = (locFare / (locQTime + locDuration)) * SEC60
                    new_row = [
                        year, month, day, did,
                        wleTripNumber, wleOperatingHour, wleFare,
                        wleProductivity,
                        locTripNumber, locInNumber, locOutNumber,
                        locQTime, locEP, locDuration, locFare,
                        QTime_locTrip, EP_locTrip,
                        locProductivity]
                    writer.writerow(new_row)


def filter_dayBased():
    for y in range(9, 11):
        yyyy = '20%02d' % y
        logger.info('handle the file; %s' % yyyy)
        for statisticsAllDriversDay_ns_prefix in [statisticsAllDriversDay_ns1517_prefix, statisticsAllDriversDay_ns2023_prefix]:
            Ydf = pd.read_csv('%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversDay_ns_prefix , yyyy))
            outlier_index = set()
            for cn in Ydf.columns:
                if cn in ['year', 'month', 'day', 'hour', 'driverID']:
                    continue
                if cn == 'wleProductivity':
                    outlier_set = set(np.where(Ydf[cn] > 80)[0].tolist())
                    outlier_index = outlier_index.union(set(outlier_set))
            Ydf = Ydf.drop(Ydf.index[list(outlier_index)])
            Ydf.to_csv('%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversDay_ns_prefix , yyyy), index=False)


def process_monthBased():
    logger.info('handle dayBased')
    #
    for y in range(9, 11):
        yyyy = '20%02d' % y
        logger.info('handle the file; %s' % yyyy)
        #
        statistics1517_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversMonth_ns1517_prefix, yyyy)
        statistics2023_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversMonth_ns2023_prefix, yyyy)
        for statisticsAllDriversDay_ns_prefix, statistics_fpath in [(statisticsAllDriversDay_ns1517_prefix, statistics1517_fpath),
                                                                    (statisticsAllDriversDay_ns2023_prefix, statistics2023_fpath)]:
            dateDid_statistics = {}
            with open('%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversDay_ns_prefix, yyyy), 'rt') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    year, month = map(int, [row[hid[cn]] for cn in ['year', 'month']])
                    if year != int(yyyy):
                        continue
                    did = int(row[hid['driverID']])
                    k = (year, month, did)
                    if not dateDid_statistics.has_key(k):
                        dateDid_statistics[k] = [0.0 for _ in [WTN, WOH, WF, LTN, LIN, LON, LQ, LEP, LD, LF]]
                    dateDid_statistics[k][WTN] += int(row[hid['wleTripNumber']])
                    dateDid_statistics[k][WOH] += float(row[hid['wleOperatingHour']])
                    dateDid_statistics[k][WF] += float(row[hid['wleFare']])
                    dateDid_statistics[k][LTN] += int(row[hid['locTripNumber']])
                    dateDid_statistics[k][LIN] += int(row[hid['locInNumber']])
                    dateDid_statistics[k][LON] += int(row[hid['locOutNumber']])
                    dateDid_statistics[k][LQ] += float(row[hid['locQTime']])
                    dateDid_statistics[k][LEP] += float(row[hid['locEP']])
                    dateDid_statistics[k][LD] += float(row[hid['locDuration']])
                    dateDid_statistics[k][LF] += float(row[hid['locFare']])
            #
            with open(statistics_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                header = ['year', 'month', 'driverID',
                          'wleTripNumber', 'wleOperatingHour', 'wleFare',
                          'wleProductivity',
                          'locTripNumber', 'locInNumber', 'locOutNumber',
                          'locQTime', 'locEP', 'locDuration', 'locFare',
                          'QTime/locTrip', 'EP/locTrip',
                          'locProductivity',
                          'locInRatio']
                writer.writerow(header)
                for (year, month, did), statistics in dateDid_statistics.iteritems():
                    wleTripNumber, wleOperatingHour, wleFare = int(statistics[WTN]), statistics[WOH], statistics[WF],
                    locTripNumber, locInNumber, locOutNumber = map(int, [statistics[LTN], statistics[LIN], statistics[LON]])
                    locQTime, locEP, locDuration, locFare = statistics[LQ], statistics[LEP], statistics[LD], statistics[LF]
                    #
                    wleProductivity = wleFare / wleOperatingHour
                    QTime_locTrip, EP_locTrip = locQTime / float(locTripNumber), locEP / float(locTripNumber)
                    locProductivity = (locFare / (locQTime + locDuration)) * SEC60
                    locInRatio = locInNumber / float(locTripNumber)
                    new_row = [
                        year, month, did,
                        wleTripNumber, wleOperatingHour, wleFare,
                        wleProductivity,
                        locTripNumber, locInNumber, locOutNumber,
                        locQTime, locEP, locDuration, locFare,
                        QTime_locTrip, EP_locTrip,
                        locProductivity,
                        locInRatio]
                    writer.writerow(new_row)

def aggregate_yearBased():
    logger.info('handle year based')
    WTN, WOH, WF, \
    LTN, LIN, LON, \
    LQ, LEP, \
    LD, LF = range(10)
    for y in range(9, 11):
        yyyy = '20%02d' % y
        statistics1517_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversYear_ns1517_prefix, yyyy)
        statistics2023_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversYear_ns2023_prefix, yyyy)
        for statisticsAllDriversMonth_ns_prefix, statistics_fpath in [
            (statisticsAllDriversMonth_ns1517_prefix, statistics1517_fpath),
            (statisticsAllDriversMonth_ns2023_prefix, statistics2023_fpath)]:
            dateDid_statistics = {}
            with open('%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversMonth_ns_prefix, yyyy), 'rt') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    year, month = map(int, [row[hid[cn]] for cn in ['year', 'month']])
                    did = int(row[hid['driverID']])
                    k = (year, did)
                    if not dateDid_statistics.has_key(k):
                        dateDid_statistics[k] = [0.0 for _ in [WTN, WOH, WF, LTN, LIN, LON, LQ, LEP, LD, LF]]
                    dateDid_statistics[k][WTN] += int(row[hid['wleTripNumber']])
                    dateDid_statistics[k][WOH] += float(row[hid['wleOperatingHour']])
                    dateDid_statistics[k][WF] += float(row[hid['wleFare']])
                    dateDid_statistics[k][LTN] += int(row[hid['locTripNumber']])
                    dateDid_statistics[k][LIN] += int(row[hid['locInNumber']])
                    dateDid_statistics[k][LON] += int(row[hid['locOutNumber']])
                    dateDid_statistics[k][LQ] += float(row[hid['locQTime']])
                    dateDid_statistics[k][LEP] += float(row[hid['locEP']])
                    dateDid_statistics[k][LD] += float(row[hid['locDuration']])
                    dateDid_statistics[k][LF] += float(row[hid['locFare']])
            with open(statistics_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                header = ['year', 'driverID',
                          'wleTripNumber', 'wleOperatingHour', 'wleFare',
                          'wleProductivity',
                          'locTripNumber', 'locInNumber', 'locOutNumber',
                          'locQTime', 'locEP', 'locDuration', 'locFare',
                          'QTime/locTrip', 'EP/locTrip',
                          'locProductivity',
                          'locInRatio']
                writer.writerow(header)
                for (year, did), statistics in dateDid_statistics.iteritems():
                    wleTripNumber, wleOperatingHour, wleFare = int(statistics[WTN]), statistics[WOH], statistics[WF],
                    locTripNumber, locInNumber, locOutNumber = map(int, [statistics[LTN], statistics[LIN], statistics[LON]])
                    locQTime, locEP, locDuration, locFare = statistics[LQ], statistics[LEP], statistics[LD], statistics[LF]
                    #
                    wleProductivity = wleFare / wleOperatingHour
                    QTime_locTrip, EP_locTrip = locQTime / float(locTripNumber), locEP / float(locTripNumber)
                    locProductivity = (locFare / (locQTime + locDuration)) * SEC60
                    locInRatio = locInNumber / float(locTripNumber)
                    new_row = [
                        year, did,
                        wleTripNumber, wleOperatingHour, wleFare,
                        wleProductivity,
                        locTripNumber, locInNumber, locOutNumber,
                        locQTime, locEP, locDuration, locFare,
                        QTime_locTrip, EP_locTrip,
                        locProductivity,
                        locInRatio]
                    writer.writerow(new_row)





if __name__ == '__main__':
    run()