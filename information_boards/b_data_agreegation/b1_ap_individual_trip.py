import __init__
#
from information_boards import dpaths, prefixs
from information_boards import HOLIDAYS2009, HOLIDAYS2010, WEEKENDS
#
from datetime import datetime
import pandas as pd
import csv


if_dpath = dpaths['qrTime_qNumber', 'ap']
if_prefix = prefixs['qrTime_qNumber', 'ap']

TH_QRTIME_MAX = 180  # Minute
TH_QRTIME_MIN = 0
TH_PRODUCTIVITY = 80  # Dollar/Hour
TH_DURATION = 1  # Minute


def run(yy):
    filtered_summary_fpath = '%s/Filtered-%s20%s.csv' % (if_dpath, if_prefix, yy)
    with open(filtered_summary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['year', 'month', 'day', 'hour', 'weekEnd',
                      'did',
                      'prevEndTerminal', 'pickUpTerminal',
                      'duration', 'fare',
                      'qrTime', 'productivity',
                      'T1', 'T2', 'T3', 'BudgetT',
                      'minTer']
        writer.writerow(new_header)
    #
    summary_fpath = '%s/%s20%s.csv' % (if_dpath, if_prefix, yy)
    holidays = HOLIDAYS2009 if yy == '09' else HOLIDAYS2010
    with open(summary_fpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        for row in reader:
            qrTime = eval(row[hid['qrTime']]) / float(60)  # Second -> Minute
            if qrTime <= TH_QRTIME_MIN or qrTime > TH_QRTIME_MAX:
                continue
            productivity = eval(row[hid['productivity']]) * 3600 / 100  # Cent/Second -> Dollar/Hour
            if productivity > TH_PRODUCTIVITY:
                continue
            duration = eval(row[hid['duration']]) / float(60)  # Second -> Minute
            if duration <= TH_DURATION:
                continue
            #
            year, month, day, hour = map(int, [row[hid[cn]] for cn in ['year', 'month', 'day', 'hour']])
            weekEnd = 0
            if (year, month, day) in holidays:
                weekEnd = 1
            if datetime(year, month, day).weekday() in WEEKENDS:
                weekEnd = 1
            fare = eval(row[hid['fare']]) / float(100)  # Cent -> Dollar
            #
            new_row = [year, month, day, hour, weekEnd]
            new_row += [row[hid[cn]] for cn in ['did']]
            new_row += [row[hid[cn]] for cn in ['prevEndTerminal', 'pickUpTerminal']]
            new_row += [duration, fare]
            new_row += [qrTime, productivity]
            new_row += [row[hid[cn]] for cn in ['T1', 'T2', 'T3', 'BudgetT']]
            new_row += [row[hid[cn]] for cn in ['minTer']]
            with open(filtered_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow(new_row)


if __name__ == '__main__':
    run('10')
