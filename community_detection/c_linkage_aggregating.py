import __init__
#
from __init__ import lc_dir, la_dir
from __init__ import REMAINING_LINKAGE_RATIO
#
from taxi_common.file_handling_functions import load_pickle_file, save_pkl_threading, save_pickle_file
from taxi_common.file_handling_functions import check_path_exist, check_dir_create
#
import datetime
from dateutil.relativedelta import relativedelta


def run():
    process_files('0904')


def process_files(yymm):
    linkage_yymm_dir = lc_dir + '/%s' % yymm
    assert check_path_exist(linkage_yymm_dir)
    edge_yymm_dir = la_dir + '/%s' % yymm
    check_dir_create(edge_yymm_dir)
    #
    yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
    #
    handling_date = datetime.date(yyyy, mm, 1)
    next_month = handling_date + relativedelta(months=1)
    while handling_date < next_month:
        print handling_date
        yyyy, mm, dd = handling_date.year, handling_date.month, handling_date.day
        edge_fn = edge_yymm_dir + '/%d%02d%02d.pkl' % (yyyy, mm, dd)
        if check_path_exist(edge_fn):
            handling_date += datetime.timedelta(days=1)
            continue
        #
        linkage_fn = linkage_yymm_dir + '/%d%02d%02d.pkl' % (yyyy, mm, dd)

        if not check_path_exist(linkage_fn):
            handling_date += datetime.timedelta(days=1)
            continue

        aggregated_linkage = {}
        print 'start reading'
        linkages = load_pickle_file(linkage_fn)
        print 'handling 0'
        arrange_linkage(linkages, aggregated_linkage)
        print 'reading....'
        #
        save_pickle_file(edge_fn, aggregated_linkage)
        handling_date += datetime.timedelta(days=1)


def process_files0(yymm):
    linkage_yymm_dir = lc_dir + '/%s' % yymm
    assert check_path_exist(linkage_yymm_dir)
    edge_yymm_dir = la_dir + '/%s' % yymm
    check_dir_create(edge_yymm_dir)
    #
    yyyy, mm = 2000 + int(yymm[:2]), int(yymm[2:])
    #
    handling_date = datetime.date(yyyy, mm, 1)
    next_month = handling_date + relativedelta(months=1)
    while handling_date < next_month:
        print handling_date
        yyyy, mm, dd = handling_date.year, handling_date.month, handling_date.day
        edge_fn = edge_yymm_dir + '/%d%02d%02d.pkl' % (yyyy, mm, dd)
        if check_path_exist(edge_fn):
            handling_date += datetime.timedelta(days=1)
            continue
        #
        linkage0_fn = linkage_yymm_dir + '/%d%02d%02d-0.pkl' % (yyyy, mm, dd)
        linkage1_fn = linkage_yymm_dir + '/%d%02d%02d-1.pkl' % (yyyy, mm, dd)
        if not check_path_exist(linkage0_fn) or not check_path_exist(linkage1_fn):
            handling_date += datetime.timedelta(days=1)
            continue
        aggregated_linkage = {}
        print 'start reading'
        linkages0 = load_pickle_file(linkage0_fn)
        print 'handling 0'
        arrange_linkage(linkages0, aggregated_linkage)
        print 'reading....'
        linkages1 = load_pickle_file(linkage1_fn)
        print 'handling 1'
        arrange_linkage(linkages1, aggregated_linkage)
        #
        # save_pkl_threading(edge_fn, aggregated_linkage)
        save_pickle_file(edge_fn, aggregated_linkage)
        # TODO
        # solve a problem that the main thread is ended before the sub-thread (writing) finishes a process
        #
        handling_date += datetime.timedelta(days=1)


def check_all_files_exists(linkage_yymm_dir, begin_date, end_date):
    all_exist = True
    checking_date = begin_date
    while checking_date <= end_date:
        fn0 = linkage_yymm_dir + '/%d%02d%02d-0.pkl' % (checking_date.year,
                                                        checking_date.month,
                                                        checking_date.day)
        if not check_path_exist(fn0):
            all_exist = False
            break
        fn1 = linkage_yymm_dir + '/%d%02d%02d-1.pkl' % (checking_date.year,
                                                        checking_date.month,
                                                        checking_date.day)
        if not check_path_exist(fn1):
            all_exist = False
            break
        checking_date += datetime.timedelta(days=1)
    return all_exist


def arrange_linkage(linkages, aggregated_linkage):
    while linkages:
        _did0, _did0_num_pickup, _did0_linkage = linkages.pop()
        for _did1, num_linkage in _did0_linkage.iteritems():
            if num_linkage < _did0_num_pickup * REMAINING_LINKAGE_RATIO:
                continue
            did0, did1 = int(_did0), int(_did1)
            if did0 > did1:
                did0, did1 = int(_did1), int(_did0)
            if not aggregated_linkage.has_key((did0, did1)):
                aggregated_linkage[(did0, did1)] = 0
            aggregated_linkage[(did0, did1)] += num_linkage


if __name__ == '__main__':
    run()