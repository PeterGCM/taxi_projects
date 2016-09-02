import __init__
#
from community_analysis import la_dir, com_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, \
                                                check_dir_create, save_pickle_file, \
                                                check_path_exist, remove_create_dir
#
import networkx as nx
import igraph as ig
import csv, datetime, community


def run():
    print 'start'
    check_dir_create(com_dir)
    #
    yyyy = '2009'
    for la_fn in get_all_files(la_dir, '%s-CD' % yyyy, '.pkl'):
        _, _, str_thD, _, _ = la_fn[:-len('.pkl')].split('-')
        thD = int(str_thD[len('thD('):-len(')')])
        thD_dir = '%s/%s' % (com_dir, '2009-CD(%d)' % thD)
        if check_path_exist(thD_dir):
            continue
        check_dir_create(thD_dir)
        summary_fpath = '%s/%s-community-summary.csv' % (thD_dir, yyyy)
        glayout_fpath = '%s/%s-glayout.pkl' % (thD_dir, yyyy)
        #
        with open(summary_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['com-name', 'num-nodes', 'num-edges', 'tie-strength(# of days encounter / # of drivers)']
            writer.writerow(new_headers)
        #
        print 'pkl file loading ...'
        pairs_day_counting = load_pickle_file('%s/%s' % (la_dir, la_fn))
        print 'Graph constructing ...'
        nxG = nx.Graph()
        for (k0, k1), num_days in pairs_day_counting.iteritems():
            nxG.add_edge(k0, k1, weight=num_days)
        del pairs_day_counting
        #
        print 'Whole graph pickling ...'
        nx.write_gpickle(nxG, '%s/%s-whole.pkl' % (thD_dir, yyyy))
        n_label, n_comId = [], []
        nxId_igId = {}
        ig_nid = 0
        print 'Partitioning ...'
        partition = community.best_partition(nxG)
        for i, com in enumerate(set(partition.values())):
            list_nodes = [nodes for nodes in partition.keys()
                          if partition[nodes] == com]
            print i, 'Saving sub-graph ...'
            sub_nxG = nxG.subgraph(list_nodes)
            com_name = 'COM(%d)' % i
            nx.write_gpickle(sub_nxG, '%s/%s-%s.pkl' % (thD_dir, yyyy, com_name))

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


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise