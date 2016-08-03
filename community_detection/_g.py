import __init__

from __init__ import graph_dir, v_dir

import community
import networkx as nx
import matplotlib.pyplot as plt

from taxi_common.file_handling_functions import load_pickle_file, get_all_files, remove_create_dir, remove_file


def run():
    assert len(get_all_files(graph_dir, '', '.pkl')) == 1
    fn = get_all_files(graph_dir, '', '.pkl').pop()
    pairs_day_counting = load_pickle_file('%s/%s' % (graph_dir, fn))
    G = nx.Graph()
    for (k0, k1), num_days in pairs_day_counting.iteritems():
        G.add_edge(k0, k1, weight=num_days)

    # first compute the best partition
    partition = community.best_partition(G)

    # drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
                               node_color=str(count / size), with_labels=True)

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()



if __name__ == '__main__':
    run()