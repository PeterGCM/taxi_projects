import __init__

from __init__ import graph_dir

from taxi_common.file_handling_functions import load_pickle_file, get_all_files, remove_create_dir, save_pickle_file


def run():
    num_months, max_num_days = 0, -1e400
    pairs_day_counting = {}
    N = set()
    for mm in range(1, 12):
        num_months += 1
        yymm = '09%02d' % mm
        graph_yymm_dir = graph_dir + '/_%s' % yymm
        assert len(get_all_files(graph_yymm_dir, '', '.pkl')) == 1
        fn = get_all_files(graph_yymm_dir, '', '.pkl').pop()
        print 'read', yymm, fn
        edge_weight = load_pickle_file('%s/%s' % (graph_yymm_dir, fn))
        for (k0, k1), num_days in edge_weight.iteritems():
            N.add(k0); N.add(k1)
            if (k0, k1) not in pairs_day_counting:
                pairs_day_counting[(k0, k1)] = 0
            pairs_day_counting[(k0, k1)] += num_days
            if max_num_days < pairs_day_counting[(k0, k1)]:
                max_num_days = pairs_day_counting[(k0, k1)]
    graph_fn = 'N(%d)-E(%d)-maxD(%d).pkl' % (len(N), len(pairs_day_counting), max_num_days)
    print 'graph saving'
    save_pickle_file('%s/%s' % (graph_dir, graph_fn), pairs_day_counting)

if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise