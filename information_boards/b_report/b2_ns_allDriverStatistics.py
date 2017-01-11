import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import shiftProDur_dpath, shiftProDur_prefix
from information_boards import economicProfit_ns_dpath, economicProfit_ns_prefix
from information_boards import statisticsAllDrivers_ns_dpath
from information_boards import statisticsAllDriversDay_ns1519_prefix, statisticsAllDriversMonth_ns1519_prefix, statisticsAllDriversTrip_ns1519_prefix
from information_boards import statisticsAllDriversDay_ns2000_prefix, statisticsAllDriversMonth_ns2000_prefix, statisticsAllDriversTrip_ns2000_prefix


from information_boards import DIn_PIn, DOut_PIn
from information_boards import SEC3600, SEC600, SEC60, CENT
from information_boards import HOLIDAYS2009, HOLIDAYS2010
from information_boards import WEEKENDS
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, get_all_files
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime

logger = get_logger()


def run():
    check_dir_create(statisticsAllDrivers_ns_dpath)
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
    for y in range(9, 11):
        yyyy = '20%02d' % y
        aggregate_monthBased(yyyy)

    for y in range(9, 11):
        yyyy = '20%02d' % y
        process_tripbased(yyyy)


def process_tripbased(yyyy):
    logger.info('handle the file; %s' % yyyy)
    #
    statistics1519_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversTrip_ns1519_prefix, yyyy)
    statistics2000_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversTrip_ns2000_prefix, yyyy)
    if check_path_exist(statistics1519_fpath):
        logger.info('The file had already been processed; %s' % yyyy)
        return
    yy = yyyy[2:]
    holidays = HOLIDAYS2009 if yyyy == '2009' else HOLIDAYS2010
    for statistics_fpath in [statistics1519_fpath, statistics2000_fpath]:
        with open(statistics_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['year', 'month', 'day', 'hour',
                      'driverID',
                      'locQTime', 'locEP', 'locDuration', 'locFare',
                      'locProductivity',
                      'locIn', 'weekEnd',
                      'timePassed', 'timePassed^2']
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
                locProductivity = locFare / ((locQTime + locDuration) * SEC60)
                locIn = 1 if int(row[hid['tripMode']]) == DIn_PIn else 0
                weekEnd = 0
                if (year, month, day) in holidays:
                    weekEnd = 1
                if datetime.datetime(year, month, day).weekday() in WEEKENDS:
                    weekEnd = 1
                timePassed = (year - 2009) * 12 + max(0, (month - 1))
                timePassed_2 = timePassed ** 2
                if hour in [15, 16, 17, 18, 19]:
                    statistics_fpath = statistics1519_fpath
                elif hour in [20, 21, 22, 23, 0]:
                    statistics_fpath = statistics2000_fpath
                else:
                    continue
                with open(statistics_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_row = [
                        year, month, day, hour,
                        did,
                        locQTime, locEP, locDuration, locFare,
                        locProductivity,
                        locIn, weekEnd,
                        timePassed, timePassed_2
                    ]
                    writer.writerow(new_row)


def aggregate_monthBased(yyyy):
    logger.info('handle the file; %s' % yyyy)
    #
    statistics1519_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversMonth_ns1519_prefix, yyyy)
    statistics2000_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversMonth_ns2000_prefix, yyyy)
    if check_path_exist(statistics1519_fpath):
        logger.info('The file had already been processed; %s' % yyyy)
        return
    yy = yyyy[2:]
    dateDid_statistics = {}
    WTN, WOH, WF, \
    LTN, LIN, LON, \
    LQ, LEP, \
    LD, LF = range(10)
    for statisticsAllDriversDay_ns_prefix, statistics_fpath in [(statisticsAllDriversDay_ns1519_prefix, statistics1519_fpath),
                                                                (statisticsAllDriversDay_ns2000_prefix, statistics2000_fpath)]:
        for dayBased_fn in get_all_files(statisticsAllDrivers_ns_dpath, '%s%s*'% (statisticsAllDriversDay_ns_prefix, yy)):
            with open('%s/%s' % (statisticsAllDrivers_ns_dpath, dayBased_fn), 'rt') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    year, month = map(int, [row[hid[cn]] for cn in ['year', 'month']])
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
                locProductivity = locFare / ((locQTime + locDuration) * SEC60)
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
    statistics1519_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversDay_ns1519_prefix, yymm)
    statistics2000_fpath = '%s/%s%s.csv' % (statisticsAllDrivers_ns_dpath, statisticsAllDriversDay_ns2000_prefix, yymm)
    if check_path_exist(statistics1519_fpath):
        logger.info('The file had already been processed; %s' % yymm)
        return
    dateDid_statistics1519, dateDid_statistics2000 = {}, {}
    WTN, WOH, WF, \
    LTN, LIN, LON, \
    LQ, LEP, \
    LD, LF = range(10)
    #
    logger.info('process locTrip; %s' % yymm)
    # with open('%s/%s%s.csv' % (economicProfit_ap_dpath, economicProfit_ap_prefix, yymm), 'rt') as r_csvfile:
    with open('%s/%s%s.csv' % (economicProfit_ns_dpath, economicProfit_ns_prefix, yymm), 'rt') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
            if hour in [15, 16, 17, 18, 19]:
                dateDid_statistics = dateDid_statistics1519
            elif hour in [20, 21, 22, 23, 0]:
                dateDid_statistics = dateDid_statistics2000
            else:
                continue
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
            year, month, day, hour = 2000 + int(row[hid['yy']]), int(row[hid['mm']]), int(row[hid['dd']]), int(row[hid['hh']])
            if hour in [15, 16, 17, 18, 19]:
                dateDid_statistics = dateDid_statistics1519
            elif hour in [20, 21, 22, 23, 0]:
                dateDid_statistics = dateDid_statistics2000
            else:
                continue
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
            day, hour = int(row[hid['day']]), int(row[hid['hour']])
            if hour in [15, 16, 17, 18, 19]:
                dateDid_statistics = dateDid_statistics1519
            elif hour in [20, 21, 22, 23, 0]:
                dateDid_statistics = dateDid_statistics2000
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
    for statistics_fpath, dateDid_statistics in [(statistics1519_fpath, dateDid_statistics1519),
                                                 (statistics2000_fpath, dateDid_statistics2000)]:
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