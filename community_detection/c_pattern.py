import __init__
#
from __init__ import MAX_LINKAGE_RATIO
from __init__ import linkage_dir
#
from taxi_common.file_handling_functions import save_pickle_file, remove_creat_dir
from taxi_common.file_handling_functions import load_pickle_file, get_fn_only, get_all_files


def run(pkl_dir):
    print pkl_dir
    assert False
    for fn in get_all_files(pkl_dir , '', '.pkl'):
        linkages = load_pickle_file(pkl_dir + '/' + fn)
        edge_weight = {}
        count = 0
        for _did0, l in linkages:
            count += 1
            num_linkages0 = [num for num in l.itervalues()]
            if not num_linkages0:
                continue
            max_linkage = max(num_linkages0)
            for _did1, num_linkage1 in l.iteritems():
                if _did1 == '-1':
                    continue
                if num_linkage1 < max_linkage * MAX_LINKAGE_RATIO:
                    continue
                did0, did1 = int(_did0), int(_did1)
                if did0 > did1:
                    did0, did1 = int(_did1), int(_did0)
                if not edge_weight.has_key((did0, did1)):
                    edge_weight[(did0, did1)] = 0
                edge_weight[(did0, did1)] += num_linkage1
            if count % 2000 == 0:
                print count
                save_pickle_file(pkl_dir + '/ft_%s.pkl' % get_fn_only(fn)[:-len('.pkl')], edge_weight)
        save_pickle_file(pkl_dir + '/ft_%s.pkl' % get_fn_only(fn)[:-len('.pkl')], edge_weight)
