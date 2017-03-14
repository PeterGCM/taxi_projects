import __init__
#
'''

'''
#
from information_boards import trip_dpath, trip_prefix
from information_boards import dpaths, prefixs
from information_boards import HOUR1, AM6
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
from taxi_common.log_handling_functions import get_logger
#
import csv

logger = get_logger()

if_dpath = trip_dpath
if_prefix = trip_prefix
of_dpath = dpaths['hourProductivity']
of_prefix = prefixs['hourProductivity']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def process_file(yymm):
    from traceback import format_exc
    try:
        logger.info('handle the file; %s' % yymm)
        ifpath = '%s/%s%s.csv' % (if_dpath, if_prefix, yymm)
        if not check_path_exist(ifpath):
            logger.info('The file X exists; %s' % yymm)
            return None
        ofpath = '%s/%s%s.csv' % (of_dpath, of_prefix, yymm)
        drivers = {}
        handling_day = 0
        with open(ifpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            with open(ofpath, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_header = header + ['hourProductivity']
                writer.writerow(new_header)
            for row in reader:
                did = int(row[hid['did']])
                if not drivers.has_key(did):
                    drivers[did] = driver(did, ofpath, hid)
                drivers[did].update_tripInstances(int(row[hid['endTime']]), row)
                if int(row[hid['day']]) != handling_day:
                    handling_day = int(row[hid['day']])
                    logger.info('processing %dth day; %s' % (handling_day, yymm))
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


class driver(object):
    def __init__(self, did, ofpath, hid):
        self.did = did
        self.handlingDay = 0
        self.ofpath, self.hid = ofpath, hid
        self.tripInstances = []

    def __repr__(self):
        return 'did %s' % str(self.did)

    def update_tripInstances(self, curEndTime, curTripInfo):
        if int(curTripInfo[self.hid['day']]) != self.handlingDay and int(curTripInfo[self.hid['hour']]) == AM6:
            self.tripInstances = []
            self.handlingDay = int(curTripInfo[self.hid['day']])
        self.tripInstances += [(curEndTime, curTripInfo)]
        indexForExclusion = 0
        for i, (prevEndTime0, prevTripInfo0) in enumerate(self.tripInstances):
            if curEndTime - prevEndTime0 > HOUR1:
                indexForExclusion += 1
                if prevTripInfo0[self.hid['prevEndTerminalAP']] == 'X':
                    continue
                hourProductivity = 0
                for prevEndTime1, prevTripInfo1 in self.tripInstances[i:]:
                    if prevEndTime1 - prevEndTime0 < HOUR1:
                        hourProductivity += int(prevTripInfo1[self.hid['fare']])
                    else:
                        timeOver = (prevEndTime0 + HOUR1) - prevEndTime1
                        hourProductivity += int(prevTripInfo1[self.hid['fare']]) * (timeOver / float(prevTripInfo1[self.hid['duration']]))
                        break
                with open(self.ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(prevTripInfo0 + [hourProductivity])
            else:
                break
        # update list
        self.tripInstances = self.tripInstances[indexForExclusion:]
