import __init__
#
from __init__ import MAX_LINKAGE_RATIO
from __init__ import linkage_dir
#
from taxi_common.file_handling_functions import save_pickle_file, remove_creat_dir, check_path_exist
from taxi_common.file_handling_functions import load_pickle_file, get_fn_only, get_all_files


def run(pkl_dir):
    for fn in get_all_files(pkl_dir , '', '.pkl'):
    	print fn
        linkages = load_pickle_file(pkl_dir + '/' + fn)
        edge_weight0 = {}
        for _did0, l in linkages:
            for _did1, num_linkage in l.iteritems():
                did0, did1 = int(_did0), int(_did1)
                if did0 > did1:
                    did0, did1 = int(_did1), int(_did0)
                if not edge_weight0.has_key((did0, did1)):
                    edge_weight0[(did0, did1)] = 0
                edge_weight0[(did0, did1)] += num_linkage
        yyyymmdd = get_fn_only(fn)[:-len('.pkl')].split('-')[0]

        saving_fn = pkl_dir + '/m_%s.pkl' % yyyymmdd
        if check_path_exist(saving_fn):
            edge_weight1 = load_pickle_file(saving_fn)
            for k, v in edge_weight1.iteritems():
                if not edge_weight0.has_key(k):
                    edge_weight0[k] = v
                else:
                    edge_weight0[k] += v
        save_pickle_file(saving_fn, edge_weight0)
