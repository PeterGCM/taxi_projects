import __init__
#
'''

'''
#
from information_boards import queueingTime_ap_dpath, queueingTime_ap_prefix
from information_boards import queueingTime_ns_dpath, queueingTime_ns_prefix
from information_boards import productivity_summary_fpath
from information_boards import economicProfit_ap_dpath, economicProfit_ap_prefix
from information_boards import economicProfit_ns_dpath, economicProfit_ns_prefix
#
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.log_handling_functions import get_logger
#
import csv, datetime

logger = get_logger()


def run():
    for dpath in [economicProfit_ap_dpath, economicProfit_ns_dpath]:
        check_dir_create(dpath)
    #
    # init_multiprocessor(6)
    # count_num_jobs = 0
    # for y in xrange(9, 11):
    #     for m in xrange(1, 13):
    #         yymm = '%02d%02d' % (y, m)
    #         if yymm in ['0912', '1010']:
    #             continue
    #         process_files(yymm)
    #         # put_task(process_files, [yymm])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)



def process_files(yymm):
    from traceback import format_exc
    try:
        logger.info('Start summary')
        yy, mm = yymm[:2], yymm[-2:]
        #
        ap_gen_productivity, ns_gen_productivity = {}, {}
        with open(productivity_summary_fpath) as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                yyyy, mm, dd, hh = 2000 + eval(row[hid['year']]), eval(row[hid['month']]), eval(row[hid['day']]), eval(
                    row[hid['hour']])
                ap_gen_productivity[(yyyy, mm, dd, hh)] = eval(row[hid['apGenProductivity']])
                ns_gen_productivity[(yyyy, mm, dd, hh)] = eval(row[hid['nsGenProductivity']])
        #
        for queueingTime_dpath, queueingTime_prefix, economicProfit_dpath, economicProfit_prefix, gen_productivity in [
            (queueingTime_ap_dpath, queueingTime_ap_prefix, economicProfit_ap_dpath, economicProfit_ap_prefix, ap_gen_productivity),
            (queueingTime_ns_dpath, queueingTime_ns_prefix, economicProfit_ns_dpath, economicProfit_ns_prefix, ns_gen_productivity)]:
            with open('%s/%s%s.csv' % (queueingTime_dpath, queueingTime_prefix, yymm), 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                with open('%s/%s%s.csv' % (economicProfit_dpath, economicProfit_prefix, yymm), 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    new_headers = ['startTime', 'did', 'duration', 'fare',
                                   'tripMode', 'queueingTime', 'economicProfit',
                                   'year', 'month', 'day', 'hour']
                    writer.writerow(new_headers)
                    #
                    for row in reader:
                        st_ts = eval(row[hid['startTime']])
                        st_dt = datetime.datetime.fromtimestamp(st_ts)
                        k = (st_dt.year, st_dt.month, st_dt.day, st_dt.hour)
                        print k
                        # print row
                        # qt = eval(row[hid['queueingTime']])
                        # dur, fare = eval(row[hid['duration']]), eval(row[hid['fare']])
                        # eco_profit = fare - gen_productivity[k] * (qt + dur)
                        # #
                        # writer.writerow([st_ts, row[hid['did']], dur, fare,
                        #                  row[hid['tripMode']], qt, eco_profit,
                        #                  yy, st_dt.month, st_dt.day, st_dt.hour])
        #
        logger.info('end the file; %s' % yymm)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymm), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run()
