import __init__
#
from community_analysis.__init__ import pg_dir
#
from taxi_common.file_handling_functions import save_pickle_file, get_all_files, check_dir_create
#
import igraph as ig
import networkx as nx
import csv


MIN_NODES = 5


def run():
    target = '2009-TH(23)'
    target_dir = '%s/%s' % (pg_dir, target)

    summary_fn = '%s/%s_summary.csv' % (target_dir, target)
    glayout_fn = '%s/%s_glayout.csv' % (target_dir, target)
    with open(summary_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['fname','num_nodes','num_edges','tie-strength','%d-top-centrality-nodes' % MIN_NODES]
        writer.writerow(new_headers)
    print 'finish init'
    whole_fn = None
    labels, group = [], []
    nx_nid_ig_nid = {}
    count, ig_nid = 0, 0
    summary = []
    for fn in get_all_files(target_dir, '', '.pkl'):
        print fn
        if fn.endswith('whole.pkl'):
            whole_fn = fn
            continue
        count += 1
        nxG = nx.read_gpickle('%s/%s' % (target_dir, fn))
        nxN = nxG.nodes()
        #
        # For visualization
        #
        for n in nxN:
            labels.append(n)
            group.append(count)
            nx_nid_ig_nid[n] = ig_nid
            ig_nid += 1
        #
        # For summary
        #
        _, _, weight = zip(*list(nxG.edges_iter(data='weight', default=1)))
        num_nodes, num_edges = len(nxN), len(weight)
        if num_nodes < MIN_NODES:
            continue
        top_nodes, _ = zip(*sorted(nx.degree_centrality(nxG).items(), key=lambda x:x[-1], reverse=True)[:5])
        summary.append(['%s/%s' % (target_dir, fn), num_nodes, num_edges, sum(weight) / float(num_nodes), top_nodes])
    print 'finish preprocessing'
    #
    nxG = nx.read_gpickle('%s/%s' % (target_dir, whole_fn))
    print 'finish loading', whole_fn
    import datetime
    print datetime.datetime.now()
    igG = ig.Graph([(nx_nid_ig_nid[n0], nx_nid_ig_nid[n1]) for (n0, n1) in nxG.edges()])
    layt = igG.layout('kk', dim=3)
    print 'finish layout calculation'
    print datetime.datetime.now()
    #
    save_pickle_file(glayout_fn, [labels, group, layt])
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