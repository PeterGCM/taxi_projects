import __init__

from __init__ import la_dir, graph_dir

from graph_tool.all import *
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, remove_create_dir, remove_file


def run():
    process_files('0901')


def process_files(yymm):
    edge_yymm_dir = la_dir + '/%s' % yymm
    graph_yymm_dir = graph_dir + '/%s' % yymm
    remove_create_dir(graph_yymm_dir)
    #
    aggregated_ew = {}
    num_days, max_weight = 0, -1e400
    N, E = set(), set()
    for fn in get_all_files(edge_yymm_dir, '', '.pkl'):
        num_days += 1
        print 'read', fn
        edge_weight = load_pickle_file('%s/%s' % (edge_yymm_dir, fn))
        for (k0, k1), v in edge_weight.iteritems():
            if not aggregated_ew.has_key((k0, k1)):
                aggregated_ew[(k0, k1)] = 0
            aggregated_ew[(k0, k1)] += v
            N.add(k0); N.add(k1); E.add((k0, k1))
            if max_weight < aggregated_ew[(k0, k1)]:
                max_weight = aggregated_ew[(k0, k1)]
    #
    lb_weight = int(max_weight * 0.3)
    ub_weight = int(max_weight * 0.9)
    print 'bound', lb_weight, ub_weight
    for threshold in range(lb_weight, ub_weight):
        print threshold,
        n, e = {}, 0
        g = Graph(directed=False)
        vprop = g.new_vertex_property('string')
        for (k0, k1), v in aggregated_ew.iteritems():
            if v < threshold:
                continue
            if k0 not in n:
                n[k0] = g.add_vertex()
                vprop[n[k0]] = str(k0)
            if k1 not in n:
                n[k1] = g.add_vertex()
                vprop[n[k1]] = str(k1)
            g.add_edge(n[k0], n[k1])
            e += 1
        print 'start drawing graph'
        graph_fn = 'D(%d)-N(%d)-E(%d)-MEW(%d)-th(%d)-n(%d)-e(%d).pdf' % (num_days,
                                                                        len(N), len(E), max_weight,
                                                                        threshold, len(n), e)
        if len(n) < 100:
            graph_draw(g, vertex_text=vprop, vertex_font_size=10, output_size=(1200, 1200), output='%s/%s'%(graph_yymm_dir, graph_fn))
        else:
            graph_draw(g, output_size=(1200, 1200), output='%s/%s' % (graph_yymm_dir, graph_fn))


if __name__ == '__main__':
    run()