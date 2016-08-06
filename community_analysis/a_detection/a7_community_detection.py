import __init__
#
from community_analysis.__init__ import pg_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, check_dir_create
#
import networkx as nx
import csv


MIN_NODES = 5

def run():
    target = '2009-TH(23)'
    target_dir = '%s/%s' % (pg_dir, target)

    summary_fn = '%s/%s_summary.csv' % (target_dir, target)
    with open(summary_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['fname','num_nodes','num_edges','tie-strength','%d-top-centrality-nodes' % MIN_NODES]
        writer.writerow(new_headers)

    summary = []
    for fn in get_all_files(target_dir, '', '.pkl'):
        if fn.endswith('whole.pkl'):
            continue
        G = nx.read_gpickle('%s/%s' % (target_dir, fn))
        _, _, weight = zip(*list(G.edges_iter(data='weight', default=1)))
        num_nodes, num_edges = len(G.nodes()), len(weight)
        if num_nodes < MIN_NODES:
            continue
        top_nodes, _ = zip(*sorted(nx.degree_centrality(G).items(), key=lambda x:x[-1], reverse=True)[:5])
        summary.append(['%s/%s' % (target_dir, fn), num_nodes, num_edges, sum(weight) / float(num_nodes), top_nodes])
    for x in sorted(summary, key=lambda x:x[-2], reverse=True):
        with open(summary_fn, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow(x)


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise