import __init__
#
from community_analysis.__init__ import pg_dir

import networkx as nx

from taxi_common.file_handling_functions import load_pickle_file, get_all_files, check_dir_create


def run():
    target_dir = pg_dir + '/2009-TH(23)'
    summary = []
    for fn in get_all_files(target_dir, '', '.pkl'):
        if fn.endswith('whole.pkl'):
            continue
        G = nx.read_gpickle('%s/%s' % (target_dir, fn))
        _, _, weight = zip(*list(G.edges_iter(data='weight', default=1)))
        num_nodes, num_edges = len(G.nodes()), len(weight)
        summary.append([fn, num_nodes, num_edges, sum(weight) / float(num_nodes)])
        print nx.degree_centrality(G).values()
    for x in sorted(summary, key=lambda x:x[-1]):
        print x



if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise