import __init__
#
from __init__ import MIN_LINKAGE, MAX_LINKAGE_RATIO
from __init__ import linkage_dir
#
from taxi_common.file_handling_functions import save_pickle_file, remove_creat_dir, check_path_exist
from taxi_common.file_handling_functions import load_pickle_file, get_fn_only, get_all_files
#
import datetime
from threading import Thread

def run(pkl_dir):
    f_yyyymmdd, t_yyyymmdd = pkl_dir.split('/')[-1].split('-')
    from_date = datetime.date(int(f_yyyymmdd[:len('yyyy')]),
                              int(f_yyyymmdd[len('yyyy'):len('yyyymm')]),
                              int(f_yyyymmdd[len('yyyymm'):]))
    to_date = datetime.date(int(t_yyyymmdd[:len('yyyy')]),
                            int(t_yyyymmdd[len('yyyy'):len('yyyymm')]),
                            int(t_yyyymmdd[len('yyyymm'):]))

    handling_date = from_date

    while handling_date < to_date:
        yyyy, mm, dd = handling_date.year, handling_date.month, handling_date.day
        print 'start reading'
        twrv0 = ThreadWithReturnValue(target=load_pickle_file, args=(pkl_dir + '/%d%02d%02d-0.pkl' % (yyyy, mm, dd),))
        twrv1 = ThreadWithReturnValue(target=load_pickle_file, args=(pkl_dir + '/%d%02d%02d-1.pkl' % (yyyy, mm, dd),))
        twrv0.start(); twrv1.start()
        #
        edge_weight = {}
        linkages0 = twrv0.join()
        print 'handling 0'
        arrage_linkage(linkages0, edge_weight)
        linkages1 = twrv1.join()
        print 'handling 1'
        arrage_linkage(linkages1, edge_weight)
        #
        saving_fn = pkl_dir + '/m_%s%s%s.pkl' % (yyyy, mm, dd)
        save_pickle_file(saving_fn, edge_weight)
        #
        handling_date += datetime.timedelta(days=1)


def arrage_linkage(linkages, edge_weight):
    while linkages:
        _did0, l = linkages.pop()
        for _did1, num_linkage in l.iteritems():
            if num_linkage < MIN_LINKAGE:
                continue
            did0, did1 = int(_did0), int(_did1)
            if did0 > did1:
                did0, did1 = int(_did1), int(_did0)
            if not edge_weight.has_key((did, did1)):
                edge_weight[(did0, did1)] = 0
            edge_weight[(did0, did1)] += num_linkage
    #
    # for _did0, l in linkages:
    #     for _did1, num_linkage in l.iteritems():
    #         did0, did1 = int(_did0), int(_did1)
    #         if did0 > did1:
    #             did0, did1 = int(_did1), int(_did0)
    #         if not edge_weight0.has_key((did0, did1)):
    #             edge_weight0[(did0, did1)] = 0
    #         edge_weight0[(did0, did1)] += num_linkage


    # for fn in get_all_files(pkl_dir , '', '.pkl'):
    # 	print fn
    #     linkages = load_pickle_file(pkl_dir + '/' + fn)
    #     edge_weight0 = {}
    #     for _did0, l in linkages:
    #         for _did1, num_linkage in l.iteritems():
    #             did0, did1 = int(_did0), int(_did1)
    #             if did0 > did1:
    #                 did0, did1 = int(_did1), int(_did0)
    #             if not edge_weight0.has_key((did0, did1)):
    #                 edge_weight0[(did0, did1)] = 0
    #             edge_weight0[(did0, did1)] += num_linkage
    #     yyyymmdd = get_fn_only(fn)[:-len('.pkl')].split('-')[0]
    #
    #     saving_fn = pkl_dir + '/m_%s.pkl' % yyyymmdd
    #     if check_path_exist(saving_fn):
    #         edge_weight1 = load_pickle_file(saving_fn)
    #         for k, v in edge_weight1.iteritems():
    #             if not edge_weight0.has_key(k):
    #                 edge_weight0[k] = v
    #             else:
    #                 edge_weight0[k] += v
    #     save_pickle_file(saving_fn, edge_weight0)


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs, Verbose)
        self._return = None
    def run(self):
        if self._Thread__target is not None:
            self._return = self._Thread__target(*self._Thread__args,
                                                **self._Thread__kwargs)
    def join(self):
        Thread.join(self)
        return self._return