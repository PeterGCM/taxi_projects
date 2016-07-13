import __init__
#
from __init__ import MIN_LINKAGE, MAX_LINKAGE_RATIO
from __init__ import linkage_dir
#
from taxi_common.file_handling_functions import save_pickle_file, remove_create_dir, check_path_exist
from taxi_common.file_handling_functions import load_pickle_file, get_fn_only, save_pkl_threading
#
import datetime

def run():
    process_files('_0901')


def process_files(yymm):


    handling_date = from_date

    while handling_date < to_date:
        print handling_date
        yyyy, mm, dd = handling_date.year, handling_date.month, handling_date.day
        #
        edge_weight = {}
        print 'start reading'
        linkages0 = load_pickle_file(pkl_dir + '/%d%02d%02d-0.pkl' % (yyyy, mm, dd))
        print 'handling 0'
        arrange_linkage(linkages0, edge_weight)
        print 'reading....'
        linkages1 = load_pickle_file(pkl_dir + '/%d%02d%02d-1.pkl' % (yyyy, mm, dd))
        print 'handling 1'
        arrange_linkage(linkages1, edge_weight)
        #
        saving_fn = pkl_dir + '/m-%s-%d%02d%02d.pkl' % (f_yyyymmdd, yyyy, mm, dd)
        save_pkl_threading(saving_fn, edge_weight)
        #
        handling_date += datetime.timedelta(days=1)


def arrange_linkage(linkages, edge_weight):
    while linkages:
        _did0, _did0_linkage = linkages.pop()
        for _did1, num_linkage in _did0_linkage.iteritems():
            did0, did1 = int(_did0), int(_did1)
            if did0 > did1:
                did0, did1 = int(_did1), int(_did0)
            if not edge_weight.has_key((did0, did1)):
                edge_weight[(did0, did1)] = 0
            edge_weight[(did0, did1)] += num_linkage


if __name__ == '__main__':
    run()