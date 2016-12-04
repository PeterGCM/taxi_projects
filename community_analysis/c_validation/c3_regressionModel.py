import __init__
#
'''

'''
#
from community_analysis import group_dpath, group_prepix
from community_analysis import pickUp_dpath, pickUp_prepix
from community_analysis import roamingTime_dpath, roamingTime_prepix
from community_analysis import regressionModel_dpath, regressionModel_prefix
from community_analysis import X_PICKUP, O_PICKUP
from community_analysis import HOUR1
#
from taxi_common.file_handling_functions import check_dir_create, get_all_directories, check_path_exist, load_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv

logger = get_logger()


def run():
    check_dir_create(regressionModel_dpath)
    #
    for wc in get_all_directories(group_dpath):
        regressionModel_wc_dpath = '%s/%s' % (regressionModel_dpath, wc)
        check_dir_create(regressionModel_wc_dpath)

    init_multiprocessor(6)
    count_num_jobs = 0
    for y in range(9, 10):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)

    # for y in range(9, 10):
    #     yyyy = '20%02d' % (y)
    #     merge_year(yyyy)


def merge_year(period):
    from traceback import format_exc
    #
    try:
        logger.info('Handle merge %s' % period)
        yy = period[2:]
        for wc in get_all_directories(regressionModel_dpath):
            #
            # if wc != 'fb':
            #     continue
            #
            regressionModel_wc_dpath = '%s/%s' % (regressionModel_dpath, wc)
            prefix = '%s%s-%s' % (regressionModel_prefix, wc, yy)
            gn_fpaths = {}
            for fn in get_all_files(regressionModel_wc_dpath, prefix, '.csv'):
                if len(fn[:-len('.csv')].split('-')) == len('regressionModel-fb-0901.csv'[:-len('.csv')].split('-')):
                    continue
                else:
                    _, _, _, gn = fn[:-len('.csv')].split('-')
                    fpath = '%s/%s' % (regressionModel_wc_dpath, fn)
                    if not gn_fpaths.has_key(gn):
                        gn_fpaths[gn] = list()
                    gn_fpaths[gn].append(fpath)
            for gn, fpaths in gn_fpaths.iteritems():
                merged_fpath = '%s/%s%s-%s-%s.csv' % (regressionModel_wc_dpath, regressionModel_prefix, wc, period, gn)
                if check_path_exist(merged_fpath):
                    continue
                for fpath in fpaths:
                    if not check_path_exist(merged_fpath):
                        with open(merged_fpath, 'wt') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            with open(fpath, 'rb') as r_csvfile:
                                reader = csv.reader(r_csvfile)
                                header = reader.next()
                                writer.writerow(header)
                    with open(merged_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        with open(fpath, 'rb') as r_csvfile:
                            reader = csv.reader(r_csvfile)
                            reader.next()
                            for row in reader:
                                writer.writerow(row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], period), 'w') as f:
            f.write(format_exc())
        raise



def process_file(period):
    from traceback import format_exc
    #
    try:
        logger.info('Handle %s' % period)
        for wc in get_all_directories(regressionModel_dpath):
            regressionModel_wc_dpath = '%s/%s' % (regressionModel_dpath, wc)
            regressionModel_fpath = '%s/%s%s-%s.csv' % (regressionModel_wc_dpath, regressionModel_prefix, wc, period)
            if check_path_exist(regressionModel_fpath):
                logger.info('Already handled %s' % regressionModel_fpath)
                return None
            #
            logger.info('Loading group drivers %s' % period)
            yyyy = '20%s' % (period[:2])
            group_wc_dpath = '%s/%s' % (group_dpath, wc)
            group_drivers_fpath = '%s/%s%s-%s-drivers.pkl' % (group_wc_dpath, group_prepix, wc, yyyy)
            group_drivers = load_pickle_file(group_drivers_fpath)
            #
            logger.info('Loading pickUp %s' % period)
            pickUp_wc_dpath = '%s/%s' % (pickUp_dpath, wc)
            pickUp_fpath = '%s/%s%s-%s.pkl' % (pickUp_wc_dpath, pickUp_prepix, wc, period)
            pickUp = load_pickle_file(pickUp_fpath)
            #
            logger.info('Loading roamingTime %s' % period)
            roamingTime_wc_dpath = '%s/%s' % (roamingTime_dpath, wc)
            roamingTime_fpath = '%s/%s%s-%s.pkl' % (roamingTime_wc_dpath, roamingTime_prepix, wc, period)
            roamingTime = load_pickle_file(roamingTime_fpath)
            #
            logger.info('Generate regression model  %s' % period)
            whole_drivers = []
            driver_gn = {}
            for gn, gn_drivers in group_drivers.iteritems():
                header = ['month', 'day', 'timeFrame', 'zi', 'zj', 'groupName', 'did', 'roamingTime']
                for did in gn_drivers:
                    whole_drivers.append(did)
                    header.append(did)
                    driver_gn[did] = gn
                regressionModel_gn_fpath = '%s/%s%s-%s-%s.csv' % \
                                           (regressionModel_wc_dpath, regressionModel_prefix, wc, period, gn)
                with open(regressionModel_gn_fpath, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(header)
            with open(regressionModel_fpath, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                header = ['month', 'day', 'timeFrame', 'zi', 'zj', 'groupName', 'did', 'roamingTime']
                header += whole_drivers
                writer.writerow(header)
            #
            old_per, per_interval = 0, 5
            for i, ((did1, month, day, timeFrame, zi, zj), rt) in enumerate(roamingTime.iteritems()):
                if rt <= 0:
                    continue
                if rt >= HOUR1:
                    continue
                gn = driver_gn[did1]
                #
                regressionModel_gn_fpath = '%s/%s%s-%s-%s.csv' % \
                                           (regressionModel_wc_dpath, regressionModel_prefix, wc, period, gn)
                with open(regressionModel_gn_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_row = [month, day, timeFrame, zi, zj,
                               gn, did1, rt]
                    for did0 in group_drivers[gn]:
                        k = (did0, month, day, timeFrame, zi, zj)
                        new_row.append(O_PICKUP if k in pickUp else X_PICKUP)
                    writer.writerow(new_row)
                #
                with open(regressionModel_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_row = [month, day, timeFrame, zi, zj,
                               gn, did1, rt]
                    for did0 in whole_drivers:
                        k = (did0, month, day, timeFrame, zi, zj)
                        new_row.append(O_PICKUP if k in pickUp else X_PICKUP)
                    writer.writerow(new_row)
                cur_per = i / float(len(roamingTime)) * 100
                if old_per + per_interval < cur_per:
                    logger.info('\t processed %.2f  %s' % (cur_per, regressionModel_fpath))
                    old_per += per_interval
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], period), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()