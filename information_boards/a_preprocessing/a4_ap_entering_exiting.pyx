import __init__
#
from information_boards import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only
from taxi_common.log_handling_functions import get_logger
#
from bisect import bisect
import csv

logger = get_logger()


if_dpath1 = dpaths['trip', 'ap']
if_prefixs1 = prefixs['trip', 'ap']
if_dpath2 = dpaths['log', 'ap']
if_prefixs2 = prefixs['log', 'ap']
#
of_dpath = dpaths['eeTime', 'ap']
of_prefixs = prefixs['eeTime', 'ap']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(yymm):
    for trip_fn in get_all_files(if_dpath1, '%s%s*' % (if_prefixs1, yymm)):
        _, _, yymmdd = trip_fn[:-len('.csv')].split('-')
        log_fpath = '%s/%s%s.csv' % (if_dpath2, if_prefixs2, yymmdd)
        trip_fpath = '%s/%s' % (if_dpath1, trip_fn)

        process_daily(log_fpath, trip_fpath)


def process_daily(log_fpath, trip_fpath):
    log_fn, trip_fn = map(get_fn_only, [log_fpath, trip_fpath])
    _, _, yymmdd = log_fn[:-len('.csv')].split('-')
    from traceback import format_exc
    try:
        ofpath = '%s/%s%s.csv' % (of_dpath, of_prefixs, yymmdd)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['vid', 'did',
                           'pickupTime', 'dropoffTime', 'duration', 'fare',
                           'enteringTime', 'exitingTime',
                           'pickUpTerminal',
                           'prevEndTerminal', 'prevTripEndTime',
                           'year', 'month', 'day', 'hour', 'dow']
            writer.writerow(new_headers)
        #
        logger.info('handle the file; %s' % log_fn)
        vehicles = {}
        with open(log_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                t = eval(row[hid['time']])
                vid = int(row[hid['vid']])
                apBasePos = row[hid['apBasePos']]
                if not vehicles.has_key(vid):
                    vehicles[vid] = vehicle(vid)
                vehicles[vid].update_trajectory(t, apBasePos)
        #
        logger.info('handle the file; %s' % trip_fn)
        with open(trip_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                prevEndTerminal, pickUpTerminal = (row[hid[cn]] for cn in ['prevEndTerminal', 'pickUpTerminal'])
                if prevEndTerminal == 'X' and pickUpTerminal == 'X':
                    continue
                vid = int(row[hid['vid']])
                startTime = eval(row[hid['startTime']])
                if not vehicles.has_key(vid):
                    continue
                enteringTime, exitingTime = vehicles[vid].find_eeTime(startTime, pickUpTerminal)
                new_row = [row[hid[cn]] for cn in ['vid', 'did',
                                                   'startTime', 'endTime', 'duration', 'fare']]
                new_row += [enteringTime, exitingTime]
                new_row += [row[hid[cn]] for cn in ['pickUpTerminal',
                                                    'prevEndTerminal', 'prevTripEndTime',
                                                    'year', 'month', 'day', 'hour', 'dow']]
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymmdd), 'w') as f:
            f.write(format_exc())
        raise


class vehicle(object):
    def __init__(self, vid):
        self.vid = vid
        self.tra_time, self.tra_loc = [], []

    def update_trajectory(self, t, loc):
        self.tra_time += [t]
        self.tra_loc += [loc]

    def find_eeTime(self, pickupTime, pickUpTerminal):
        i = bisect(self.tra_time, pickupTime)
        if i == len(self.tra_loc):
            entering_time, exiting_time = self.tra_time[i - 1], 1e400
        else:
            loc0, loc1 = self.tra_loc[i - 1], self.tra_loc[i]
            if loc0 == pickUpTerminal:
                entering_time, exiting_time = self.tra_time[i - 1], self.tra_time[i]
            elif loc1 == pickUpTerminal:
                if i + 1 == len(self.tra_loc):
                    entering_time, exiting_time = self.tra_time[i], 1e400
                else:
                    entering_time, exiting_time = self.tra_time[i],  self.tra_time[i + 1]
            else:
                entering_time, exiting_time = 1e400, 1e400
        return entering_time, exiting_time


if __name__ == '__main__':
    run('0901')
