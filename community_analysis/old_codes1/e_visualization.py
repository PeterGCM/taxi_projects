import __init__

from __init__ import graph_dir, v_dir

from graph_tool.all import *
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, remove_create_dir, remove_file


def run():
    # for i in range(1,32):
    #     process_files('0901_%02d-%02d' % (i, i))
    process_files('0904')
    # process_files('0903_cd')


def process_files(yymm):
    graph_yymm_dir = graph_dir + '/%s' % yymm
    v_yymm_dir = v_dir + '/%s' % yymm
    remove_create_dir(v_yymm_dir)
    #
    num_n_e_set = set()
    for fn in sorted(get_all_files(graph_yymm_dir, '', '.pkl')):
        _, _, _, _, _, _n, _e = fn[:-len('.pkl')].split('-')
        num_n, num_e = int(_n[len('n('):-len(')')]), int(_e[len('e('):-len(')')])
        # if num_n < num_e:
        #     continue
        if (num_n, num_e) in num_n_e_set:
            continue
        num_n_e_set.add((num_n, num_e))
        ns = {}
        print fn,
        edges = load_pickle_file('%s/%s' % (graph_yymm_dir, fn))
        g = Graph(directed=False)
        vprop = g.new_vertex_property('string')
        for n0, n1 in edges:
            if n0 not in ns:
                ns[n0] = g.add_vertex()
                vprop[ns[n0]] = str(n0)
            if n1 not in ns:
                ns[n1] = g.add_vertex()
                vprop[ns[n1]] = str(n1)
            g.add_edge(ns[n0], ns[n1])
        v_fn = '%s/%s.pdf' % (v_yymm_dir, fn[:-len('.pkl')])
        print 'start drawing'
        if len(ns) < 400:
            graph_draw(g, vertex_text=vprop, vertex_font_size=10, output_size=(1200, 1200), output=v_fn)
        else:
            graph_draw(g, output_size=(1200, 1200), output=v_fn)


if __name__ == '__main__':
    run()