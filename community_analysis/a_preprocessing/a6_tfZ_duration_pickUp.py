import __init__
#
'''

'''
#
from community_analysis import tfZ_DP_dpath, tfZ_DP_prepix
from community_analysis import tfZ_duration_dpath, tfZ_duration_prepix
from community_analysis import tfZ_pickUp_dpath, tfZ_pickUp_prepix


from community_analysis import group_dpath, group_prepix


from community_analysis import roamingTime_dpath, roamingTime_prepix
from community_analysis import regressionModel_dpath, regressionModel_prefix
from community_analysis import X_PICKUP, O_PICKUP
from community_analysis import HOUR1
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.file_handling_functions import check_dir_create, get_all_directories, check_path_exist, load_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv

logger = get_logger()


def run():
    check_dir_create(tfZ_DP_dpath)
    #
    init_multiprocessor(6)
    count_num_jobs = 0
    for y in range(9, 10):
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            process_file(yymm)
            # put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)
    #
    # for y in range(9, 10):
    #     yyyy = '20%02d' % (y)
    #     merge_year(yyyy)


def process_file(yymm):
    from traceback import format_exc
    #
    try:
        logger.info('Handle %s' % yymm)
        yy, mm = yymm[:2], yymm[-2:]
        yyyy = '20%s' % yy
        tfZ_DP_fpath = '%s/%s%s.csv' % (tfZ_DP_dpath, tfZ_DP_prepix, yymm)
        ss_drivers_fpath = '%s/%s%s.pkl' % (ss_drivers_dpath, ss_drivers_prefix, yyyy)
        tfZ_pickUp_fpath = '%s/%s%s.pkl' % (tfZ_pickUp_dpath, tfZ_pickUp_prepix, yymm)
        tfZ_duration_fpath = '%s/%s%s.pkl' % (tfZ_duration_dpath, tfZ_duration_prepix, yymm)
        if check_path_exist(tfZ_DP_fpath):
            logger.info('Already handled %s' % yymm)
            return None
        #
        logger.info('loading ss drivers %s' % yymm)
        ss_drivers = load_pickle_file(ss_drivers_fpath)
        #
        logger.info('Loading pickUp %s' % yymm)
        pickUp = load_pickle_file(tfZ_pickUp_fpath)
        #
        logger.info('Loading roamingTime %s' % yymm)
        tfZ_duration = load_pickle_file(tfZ_duration_fpath)
        #
        logger.info('Generate duration-pickUp %s' % yymm)
        with open(tfZ_DP_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did', 'roamingTime']
            for did in ss_drivers:
                header.append(did)
            writer.writerow(header)
        #
        old_per, per_interval = 0, 5
        for i, ((did1, month, day, timeFrame, zi, zj), rt) in enumerate(tfZ_duration.iteritems()):
            if rt <= 0:
                continue
            if rt >= HOUR1:
                continue
            tfZ = '(%d,%d,%d)' % (timeFrame, zi, zj)
            with open(tfZ_DP_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = [month, day, timeFrame, zi, zj,
                           tfZ, did1, rt]
                for did0 in ss_drivers:
                    k = (did0, month, day, timeFrame, zi, zj)
                    new_row.append(O_PICKUP if k in pickUp else X_PICKUP)
                writer.writerow(new_row)
            cur_per = i / float(len(tfZ_duration)) * 100
            if old_per + per_interval < cur_per:
                logger.info('\t processed %.2f  %s' % (cur_per, yymm))
                old_per += per_interval
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


def merge_year(yymm):
    from traceback import format_exc
    #
    try:
        logger.info('Handle merge %s' % yymm)
        yy = yymm[2:]

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
            merged_fpath = '%s/%s%s-%s-%s.csv' % (regressionModel_wc_dpath, regressionModel_prefix, wc, yymm, gn)
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
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise




if __name__ == '__main__':
    run()