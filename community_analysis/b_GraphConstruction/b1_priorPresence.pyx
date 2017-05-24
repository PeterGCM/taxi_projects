import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import X_PRESENCE, O_PRESENCE
#
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime

logger = get_logger()
# numWorker = 6
# numReducers = numWorker * 10
numReducers = 11
#
year = '20%02d' % 9
depVar = 'roamingTime'
# depVar = 'interTravelTime'
#
if_dpath = dpaths['prevDrivers']
if_prefixs = prefixs['prevDrivers']
of_dpath = dpaths[depVar, 'priorPresence']
of_prefixs = prefixs[depVar, 'priorPresence']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(moduloIndex):
    logger.info('loading driversRelations %s; %s' % (year, depVar))
    superSet_fpath = '%s/%sFiltered-superSet-%s%s.pkl' % (if_dpath, depVar, if_prefixs, year)
    driversRelations = load_pickle_file(superSet_fpath)
    whole_drivers = driversRelations.keys()
    driver_subsets = [[] for _ in range(numReducers)]
    for i, did in enumerate(whole_drivers):
        driver_subsets[i % numReducers] += [did]
    for i, did1 in enumerate(whole_drivers):
        if i % numReducers != moduloIndex:
            continue
        process_files(did1, driversRelations[did1])


def process_files(did1, pickUp_drivers):
    from traceback import format_exc
    #
    try:
        logger.info('Handle arrange %s(%d)' % (year, did1))
        priorPresence_fpath = '%s/%s%s-%d.csv' % (of_dpath, of_prefixs, year, did1)
        with open(priorPresence_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['month', 'day',
                      'hour', 'zi', 'zj',
                      'did', depVar]
            for did0 in pickUp_drivers:
                header.append(did0)
            writer.writerow(header)
        yy = year[2:]
        for fn in get_all_files(if_dpath, '%sFiltered-%s%s*.csv' % (depVar, if_prefixs, yy)):
            prevDriverDefined_fpath = '%s/%s' % (if_dpath, fn)
            logger.info('Handling %s(%d); %s' % (year, did1, fn))
            with open(prevDriverDefined_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                header = reader.next()
                hid = {h: i for i, h in enumerate(header)}
                handling_day = 0
                for row in reader:
                    cur_dtT = datetime.datetime.fromtimestamp(eval(row[hid['time']]))
                    if handling_day != cur_dtT.day:
                        handling_day = cur_dtT.day
                        logger.info('Processing %s %dth day; reducer %d' % (fn, cur_dtT.day, did1))
                    if int(row[hid['did']]) != did1:
                        continue
                    _prevDrivers = row[hid['prevDrivers']].split('&')
                    if len(_prevDrivers) == 1 and _prevDrivers[0] == '':
                        continue
                    prevDrivers = map(int, _prevDrivers)
                    hour = row[hid['hour']]
                    zi, zj = row[hid['zi']], row[hid['zj']]
                    with open(priorPresence_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [row[hid['month']], row[hid['day']],
                                   hour, zi, zj,
                                   did1, row[hid[depVar]]]
                        for did0 in pickUp_drivers:
                            new_row.append(O_PRESENCE if did0 in prevDrivers else X_PRESENCE)
                        writer.writerow(new_row)
        logger.info('Finish %s(%d)' % (year, did1))
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], year), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run(0)
