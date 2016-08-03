import __init__

from __init__ import la_dir, graph_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, remove_create_dir, save_pickle_file
#


def run():
    from traceback import format_exc
    try:
        for mm in range(1, 12):
            process_files_counting_day('09%02d' % mm)
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise


def process_files_counting_day(yymm):
    la_yymm_dir = la_dir + '/%s' % yymm
    graph_yymm_dir = graph_dir + '/_%s' % yymm
    remove_create_dir(graph_yymm_dir)
    #
    num_days, max_num_days, min_num_days = 0, -1e400, 1e400
    pairs_day_counting = {}
    N = set()
    for fn in get_all_files(la_yymm_dir, '', '.pkl'):
        daily_pairs = set()
        num_days += 1
        print 'read', fn
        edge_weight = load_pickle_file('%s/%s' % (la_yymm_dir, fn))
        for (k0, k1), v in edge_weight.iteritems():
            N.add(k0); N.add(k1)
            if (k0, k1) not in daily_pairs:
                daily_pairs.add((k0, k1))
                if (k0, k1) not in pairs_day_counting:
                    pairs_day_counting[(k0, k1)] = 0
                pairs_day_counting[(k0, k1)] += 1
                if max_num_days < pairs_day_counting[(k0, k1)]:
                    max_num_days = pairs_day_counting[(k0, k1)]
                if pairs_day_counting[(k0, k1)] < min_num_days:
                    min_num_days = pairs_day_counting[(k0, k1)]

    n, e = set(), 0
    g = []
    threshold = 2
    for (k0, k1), v in pairs_day_counting.iteritems():
        if v < threshold:
            continue
        n.add(k0); n.add(k1)
        g.append([(k0, k1), v])
        e += 1
    graph_fn = 'D(%d)-N(%d)-maxD(%d)-minD(%d)-th(%d)-n(%d)-e(%d).pkl' % (num_days, len(N), max_num_days, min_num_days,
                                                                     threshold, len(n), e)
    print 'graph saving'
    save_pickle_file('%s/%s' % (graph_yymm_dir, graph_fn), g)

if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise