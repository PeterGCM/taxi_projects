import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import shiftProDur_dpath, shiftProDur_prefix
from information_boards import economicProfit_ap_dpath, economicProfit_ap_prefix
from information_boards import statisticsAllDrivers_ap_dpath
from information_boards import statisticsAllDriversDay_ap_prefix, statisticsAllDriversMonth_ap_prefix, statisticsAllDriversTrip_ap_prefix
from information_boards import statisticsAllDriversYear_ap_prefix
from information_boards import DIn_PIn, DOut_PIn
from information_boards import SEC3600, SEC60, CENT
from information_boards import HOLIDAYS2009, HOLIDAYS2010
from information_boards import WEEKENDS
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, get_all_files
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime
import numpy as np
import pandas as pd

logger = get_logger()


def run():
    check_dir_create(statisticsAllDrivers_ap_dpath)
    #
    # process_tripbased()
    filter_tripbased()
    #
    # init_multiprocessor(11)
    # count_num_jobs = 0
    # for y in xrange(9, 11):
    #     for m in xrange(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         if yymm in ['0912', '1010']:
    #             # both years data are corrupted
    #             continue
    #         # process_month(yymm)
    #         put_task(aggregate_dayBased, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)
    #
    # for y in range(9, 11):
    #     yyyy = '20%02d' % y
    #     aggregate_monthBased(yyyy)
    # aggregate_yearBased()
    #


def process_tripbased():
    for y in range(9, 11):
        yyyy = '20%02d' % y
        logger.info('handle the file; %s' % yyyy)
        #
        statistics_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix, yyyy)
        if check_path_exist(statistics_fpath):
            logger.info('The file had already been processed; %s' % yyyy)
            return
        yy = yyyy[2:]
        holidays = HOLIDAYS2009 if yyyy == '2009' else HOLIDAYS2010
        with open(statistics_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['year', 'month', 'day', 'hour',
                      'driverID',
                      'locQTime', 'locEP', 'locDuration', 'locFare',
                      'locProductivity',
                      'locIn', 'weekEnd']
            writer.writerow(header)
            for fn in get_all_files(economicProfit_ap_dpath, '%s%s*' % (economicProfit_ap_prefix, yy)):
                with open('%s/%s' % (economicProfit_ap_dpath, fn), 'rt') as r_csvfile:
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
                        new_row = [
                            year, month, day, hour,
                            did,
                            locQTime, locEP, locDuration, locFare,
                            locProductivity,
                            locIn, weekEnd,
                        ]
                        writer.writerow(new_row)


def filter_tripbased():
    for y in range(9, 11):
        yyyy = '20%02d' % y
        logger.info('handle the file; %s' % yyyy)
        Ydf = pd.read_csv('%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix, yyyy))
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
        Ydf.to_csv('%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversTrip_ap_prefix, yyyy), index=False)


def aggregate_yearBased():
    logger.info('handle year based')
    WTN, WOH, WF, \
    LTN, LIN, LON, \
    LQ, LEP, \
    LD, LF = range(10)
    for y in range(9, 11):
        yyyy = '20%02d' % y
        statistics_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversYear_ap_prefix, yyyy)
        dateDid_statistics = {}
        with open('%s/Filtered-%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversMonth_ap_prefix, yyyy), 'rt') as r_csvfile:
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


def aggregate_monthBased(yyyy):
    logger.info('handle the file; %s' % yyyy)
    #
    statistics_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversMonth_ap_prefix, yyyy)
    if check_path_exist(statistics_fpath):
        logger.info('The file had already been processed; %s' % yyyy)
        return
    yy = yyyy[2:]
    dateDid_statistics = {}
    WTN, WOH, WF, \
    LTN, LIN, LON, \
    LQ, LEP, \
    LD, LF = range(10)
    # for dayBased_fn in get_all_files(statisticsAllDrivers_ap_dpath, '%s%s*' % (statisticsAllDriversDay_ap_prefix, yy)):
    with open('%s/Filtered-%sall.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversDay_ap_prefix), 'rt') as r_csvfile:
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
                  'locInRatio',
                  'timePassed', 'timePassed^2']
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
            timePassed = (year - 2009) * 12 + max(0, (month - 1))
            timePassed_2 = timePassed ** 2
            new_row = [
                year, month, did,
                wleTripNumber, wleOperatingHour, wleFare,
                wleProductivity,
                locTripNumber, locInNumber, locOutNumber,
                locQTime, locEP, locDuration, locFare,
                QTime_locTrip, EP_locTrip,
                locProductivity,
                locInRatio,
                timePassed, timePassed_2]
            writer.writerow(new_row)


def aggregate_dayBased(yymm):
    logger.info('handle the file; %s' % yymm)
    #
    statistics_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ap_dpath, statisticsAllDriversDay_ap_prefix, yymm)
    if check_path_exist(statistics_fpath):
        logger.info('The file had already been processed; %s' % yymm)
        return
    dateDid_statistics = {}
    WTN, WOH, WF, \
    LTN, LIN, LON, \
    LQ, LEP, \
    LD, LF = range(10)
    #
    logger.info('process locTrip; %s' % yymm)
    with open('%s/%s%s.csv' % (economicProfit_ap_dpath, economicProfit_ap_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            year, month, day = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day']])
            did = int(row[hid['did']])
            k = (year, month, day, did)
            if not dateDid_statistics.has_key(k):
                dateDid_statistics[k] = [0.0 for _ in [WTN, WOH, WF, LTN, LIN, LON, LQ, LEP, LD, LF]]
            dateDid_statistics[k][LTN] += 1
            if int(row[hid['tripMode']]) == DIn_PIn:
                dateDid_statistics[k][LIN] += 1
            else:
                assert int(row[hid['tripMode']]) == DOut_PIn
                dateDid_statistics[k][LON] += 1
            dateDid_statistics[k][LQ] += float(row[hid['queueingTime']]) / SEC60
            dateDid_statistics[k][LEP] += float(row[hid['economicProfit']]) / CENT
            dateDid_statistics[k][LD] += float(row[hid['duration']]) / SEC60
            dateDid_statistics[k][LF] += float(row[hid['fare']]) / CENT
    #
    logger.info('process shift; %s' % yymm)
    with open('%s/%s%s.csv' % (shiftProDur_dpath, shiftProDur_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            year, month, day = 2000 + int(row[hid['yy']]), int(row[hid['mm']]), int(row[hid['dd']])
            did = int(row[hid['did']])
            k = (year, month, day, did)
            if not dateDid_statistics.has_key(k):
                continue
            dateDid_statistics[k][WOH] += (float(row[hid['pro-dur']]) * SEC60) / SEC3600
    #
    logger.info('process trip; %s' % yymm)
    yy, mm = yymm[:2], yymm[-2:]
    year, month = 2000 + int(yy), int(mm)
    with open('%s/%s%s.csv' % (trip_dpath, trip_prefix, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            day = int(row[hid['day']])
            did = int(row[hid['did']])
            k = (year, month, day, did)
            if not dateDid_statistics.has_key(k):
                continue
            dateDid_statistics[k][WTN] += 1
            dateDid_statistics[k][WF] += float(row[hid['fare']]) / CENT
    #
    logger.info('write statistics; %s' % yymm)
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


if __name__ == '__main__':
    run()