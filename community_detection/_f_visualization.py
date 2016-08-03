import __init__

from __init__ import graph_dir, v_dir

from graph_tool.all import *
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, remove_create_dir, remove_file


def run():
    assert len(get_all_files(graph_dir, '', '.pkl')) == 1
    fn = get_all_files(graph_dir, '', '.pkl').pop()
    pairs_day_counting = load_pickle_file('%s/%s' % (graph_dir, fn))

    g = Graph(directed=False)
    vprop = g.new_vertex_property('string')
    ns = {}
    for n0, n1 in pairs_day_counting.iterkeys():
        if n0 not in ns:
            ns[n0] = g.add_vertex()
            vprop[ns[n0]] = str(n0)
        if n1 not in ns:
            ns[n1] = g.add_vertex()
            vprop[ns[n1]] = str(n1)
        g.add_edge(ns[n0], ns[n1])
    v_fn = '%s/%s.pdf' % (graph_dir, fn[:-len('.pkl')])
    print 'start drawing'
    if len(ns) < 400:
        graph_draw(g, vertex_text=vprop, vertex_font_size=10, output_size=(1200, 1200), output=v_fn)
    else:
        graph_draw(g, output_size=(1200, 1200), output=v_fn)


if __name__ == '__main__':
    run()