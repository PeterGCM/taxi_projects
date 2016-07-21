import __init__

from __init__ import la_dir, graph_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, remove_create_dir, save_pickle_file
#
import datetime
from dateutil.relativedelta import relativedelta

def run():
    from traceback import format_exc
    try:
        # process_files('0901')
        process_within_month('0901')
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise


def process_within_month(yymm):
    yy, mm = yymm[:2], yymm[2:]
    first_dt = datetime.datetime(2000 + int(yy), int(mm), 1, 0)
    last_dt = first_dt + relativedelta(months=1) - datetime.timedelta(days=1)
    until_middle = int((last_dt - first_dt).days / float(2))
    #
    middle_dt0 = first_dt + datetime.timedelta(days=until_middle) - datetime.timedelta(days=1)
    middle_dt1 = middle_dt0 + datetime.timedelta(days=1)
    #
    day_aggregation_graph(yymm, first_dt, middle_dt0)
    day_aggregation_graph(yymm, middle_dt1, last_dt)


def day_aggregation_graph(yymm, begin_dt, end_dt):
    la_yymm_dir = la_dir + '/%s' % yymm
    graph_yymm_dir = graph_dir + '/%s_%02d-%02d' % (yymm, begin_dt.day, end_dt.day)
    remove_create_dir(graph_yymm_dir)
    h_dt = datetime.date(begin_dt.year, begin_dt.month, begin_dt.day)
    aggregated_lk = {}
    num_days, max_weight, min_weight = 0, -1e400, 1e400
    N, E = set(), set()
    while h_dt <= end_dt:
        num_days += 1
        fn = '%d%02d%02d.pkl' % (h_dt.year, h_dt.month, h_dt.day)
        print 'read', fn
        edge_weight = load_pickle_file('%s/%s' % (la_yymm_dir, fn))
        for (k0, k1), v in edge_weight.iteritems():
            if not aggregated_lk.has_key((k0, k1)):
                aggregated_lk[(k0, k1)] = 0
            aggregated_lk[(k0, k1)] += v
            N.add(k0);
            N.add(k1);
            E.add((k0, k1))
            if max_weight < aggregated_lk[(k0, k1)]:
                max_weight = aggregated_lk[(k0, k1)]
            if aggregated_lk[(k0, k1)] < min_weight:
                min_weight = aggregated_lk[(k0, k1)]
        h_dt += datetime.timedelta(days=1)

    print 'bound', min_weight, max_weight
    for threshold in range(min_weight, max_weight):
        print threshold,
        n, e = set(), 0
        g = []
        for (k0, k1), v in aggregated_lk.iteritems():
            if v < threshold:
                continue
            n.add(k0);
            n.add(k1)
            g.append((k0, k1))
            e += 1
        graph_fn = 'D(%d)-N(%d)-E(%d)-MEW(%d)-th(%d)-n(%d)-e(%d).pkl' % (num_days,
                                                                         len(N), len(E), max_weight,
                                                                         threshold, len(n), e)
        print 'graph saving'
        save_pickle_file('%s/%s' % (graph_yymm_dir, graph_fn), g)


def process_files(yymm):
    la_yymm_dir = la_dir + '/%s' % yymm
    graph_yymm_dir = graph_dir + '/%s' % yymm
    remove_create_dir(graph_yymm_dir)
    #
    aggregated_lk = {}
    num_days, max_weight, min_weight = 0, -1e400, 1e400
    N, E = set(), set()
    for fn in get_all_files(la_yymm_dir, '', '.pkl'):
        num_days += 1
        print 'read', fn
        edge_weight = load_pickle_file('%s/%s' % (la_yymm_dir, fn))
        for (k0, k1), v in edge_weight.iteritems():
            if not aggregated_lk.has_key((k0, k1)):
                aggregated_lk[(k0, k1)] = 0
            aggregated_lk[(k0, k1)] += v
            N.add(k0); N.add(k1); E.add((k0, k1))
            if max_weight < aggregated_lk[(k0, k1)]:
                max_weight = aggregated_lk[(k0, k1)]
            if aggregated_lk[(k0, k1)] < min_weight:
                min_weight = aggregated_lk[(k0, k1)]
    #
    # lb_weight = int(max_weight * 0.5)
    # ub_weight = int(max_weight * 0.95)
    print 'bound', min_weight, max_weight
    for threshold in range(min_weight, max_weight):
        print threshold,
        n, e = set(), 0
        g = []
        for (k0, k1), v in aggregated_lk.iteritems():
            if v < threshold:
                continue
            n.add(k0); n.add(k1)
            g.append((k0, k1))
            e += 1
        graph_fn = 'D(%d)-N(%d)-E(%d)-MEW(%d)-th(%d)-n(%d)-e(%d).pkl' % (num_days,
                                                                        len(N), len(E), max_weight,
                                                                        threshold, len(n), e)
        print 'graph saving'
        save_pickle_file('%s/%s' % (graph_yymm_dir, graph_fn), g)


if __name__ == '__main__':
    process_within_month('0901')
    # run()