import __init__
#
'''

'''
#
from community_analysis import prevDriversDefined_dpath, prevDriversDefined_prefix
# from community_analysis import driversRelations2009_fpath
from community_analysis import driversRelations_fpaths
from community_analysis import tfZ_TP_dpath, tfZ_TP_prefix
from community_analysis import X_PRESENCE, O_PRESENCE
#
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime

logger = get_logger()


def run():
    check_dir_create(tfZ_TP_dpath)
    numWorker = 6
    init_multiprocessor(numWorker)
    count_num_jobs = 0
    numReducers = numWorker * 10
    #
    yyyy = '20%02d' % 11
    logger.info('loading driversRelations %s' % yyyy)
    driversRelations = load_pickle_file(driversRelations_fpaths[yyyy])
    whole_drivers = driversRelations.keys()
    driver_subsets = [[] for _ in range(numReducers)]
    for i, did in enumerate(whole_drivers):
        driver_subsets[i % numReducers].append(did)
    for i, driver_subset in enumerate(driver_subsets):
        # process_files(yyyy, i, driver_subset, driversRelations)
        pickUp_drivers = set()
        for did1 in driver_subset:
            pickUp_drivers = pickUp_drivers.union(driversRelations[did1])
        put_task(process_files, [yyyy, i, driver_subset, pickUp_drivers])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yyyy, reducerID, driver_subset, pickUp_drivers):
    from traceback import format_exc
    #
    try:
        logger.info('Handle arrange %s(%d)' % (yyyy, reducerID))
        tfZ_TP_fpath = '%s/%s%s-%d.csv' % (tfZ_TP_dpath, tfZ_TP_prefix, yyyy, reducerID)
        with open(tfZ_TP_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['month', 'day',
                      'timeFrame', 'zi', 'zj', 'tfZ',
                      'did', 'spendingTime', 'roamingTime']
            for did0 in pickUp_drivers:
                header.append(did0)
            writer.writerow(header)
        yy = yyyy[2:]
        for fn in get_all_files(prevDriversDefined_dpath, 'Filtered-%s%s*.csv' % (prevDriversDefined_prefix, yy)):
            prevDriverDefined_fpath = '%s/%s' % (prevDriversDefined_dpath, fn)
            logger.info('Handling %s(%d); %s' % (yyyy, reducerID, fn))
            with open(prevDriverDefined_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                header = reader.next()
                hid = {h: i for i, h in enumerate(header)}
                handling_day = 0
                for row in reader:
                    cur_dtT = datetime.datetime.fromtimestamp(eval(row[hid['time']]))
                    if handling_day != cur_dtT.day:
                        handling_day = cur_dtT.day
                        logger.info('Processing %s %dth day; reducer %d' % (fn, cur_dtT.day, reducerID))
                    did1 = int(row[hid['did']])
                    if did1 not in driver_subset:
                        continue
                    _prevDrivers = row[hid['prevDrivers']].split('&')
                    if len(_prevDrivers) == 1 and _prevDrivers[0] == '':
                        continue
                    prevDrivers = map(int, _prevDrivers)
                    tf = row[hid['timeFrame']]
                    zi, zj = row[hid['zi']], row[hid['zj']]
                    tfZ = '(%s,%s,%s)' % (tf, zi, zj)
                    with open(tfZ_TP_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [row[hid['month']], row[hid['day']],
                                   tf, zi, zj, tfZ,
                                   did1, row[hid['spendingTime']], row[hid['roamingTime']]
                        ]
                        for did0 in pickUp_drivers:
                            new_row.append(O_PRESENCE if did0 in prevDrivers else X_PRESENCE)
                        writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yyyy), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
