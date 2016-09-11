import __init__
#
from community_analysis import la_dir, com_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, \
                                                check_dir_create, save_pickle_file, \
                                                check_path_exist
#
import networkx as nx
import igraph as ig
import csv, datetime, community


def run():
    print 'start'
    check_dir_create(com_dir)
    #
    yyyy = '2009'
    la_fn = '2009-CD(184)-N(7003)-E(5717371).pkl'
    la_fpath = '%s/%s' % (la_dir, la_fn)
    _, str_CD, _, _ = la_fn[:-len('.pkl')].split('-')
    CD = int(str_CD[len('CD('):-len(')')])
    print 'pick file loading...'
    pairs_day_counting = load_pickle_file(la_fpath)
    print 'finished'
    for thD in [18, 36, 55, 73, 82, 92]:
        thD_dpath = '%s/%s' % (com_dir, '2009-CD(%d)-thD(%d)' % (CD, thD))
        check_dir_create(thD_dpath)
        summary_fpath = '%s/%s-CD(%d)-thD(%d)-community-summary.csv' % (thD_dpath, yyyy, CD, thD)
        glayout_fpath = '%s/%s-CD(%d)-thD(%d)-glayout.pkl' % (thD_dpath, yyyy, CD, thD)
        with open(summary_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['com-name', 'num-nodes', 'num-edges', 'tie-strength(# of days encounter / # of drivers)']
            writer.writerow(new_headers)
        #
        nxG = nx.Graph()
        for (k0, k1), num_days in pairs_day_counting.iteritems():
            if num_days < thD:
                continue
            nxG.add_edge(k0, k1, weight=num_days)

        print 'Whole graph pickling ...', yyyy, CD, thD
        nx.write_gpickle(nxG, '%s/%s-CD(%d)-thD(%d)-whole-N(%d)-E(%d).pkl' % (thD_dpath, yyyy, CD, thD,
                                                                              len(nxG.nodes()), len(nxG.edges())))
        n_label, n_comId = [], []
        nxId_igId = {}
        ig_nid = 0
        print 'Partitioning ...'
        partition = community.best_partition(nxG)
        for i, com in enumerate(set(partition.values())):
            list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
            print i, 'Saving sub-graph ...'
            sub_nxG = nxG.subgraph(list_nodes)
            com_name = 'COM(%d)' % i
            com_fpath = '%s/%s-CD(%d)-thD(%d)-%s-N(%d)-E(%d).pkl' % (thD_dpath, yyyy, CD, thD,
                                                               com_name, len(sub_nxG.nodes()), len(sub_nxG.edges()))
            nx.write_gpickle(sub_nxG, com_fpath)

            _, _, weight = zip(*list(sub_nxG.edges_iter(data='weight', default=1)))
            num_nodes, num_edges = len(sub_nxG), len(weight)
            with open(summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([com_name, num_nodes, num_edges, sum(weight) / float(num_nodes)])
            #
            print i, 'labeling...'
            for n in sub_nxG.nodes():
                n_label.append(n)
                n_comId.append(i)
                nxId_igId[n] = ig_nid
                ig_nid += 1
        #
        if len(nxG.nodes()) < 1000:
            print 'Layout calculating...'
            print datetime.datetime.now()
            Edges = [(nxId_igId[n0], nxId_igId[n1]) for (n0, n1) in nxG.edges()]
            print 'finish edge converting', len(Edges)
            print datetime.datetime.now()
            igG = ig.Graph(Edges, directed=False)
            layt = igG.layout('kk', dim=3)
            print 'finish layout calculation'
            print datetime.datetime.now()
            #
            save_pickle_file(glayout_fpath, [n_label, n_comId, layt, Edges])
        else:
            save_pickle_file(glayout_fpath, [])


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise