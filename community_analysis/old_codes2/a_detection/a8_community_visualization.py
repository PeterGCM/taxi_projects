import __init__


import community
import networkx as nx
import matplotlib.pyplot as plt


def run():
    G = nx.read_gpickle('/Users/JerryHan88/PycharmProjects/taxi_projects/community_analysis/data_20160826/partitioned_group/2009-TH(30)-whole.pkl')
    # first compute the best partition
    partition = community.best_partition(G)
    print 'Partitioning finished'
    # drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()):
        count = count + 1.
        print count
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
                               node_color=str(count / float(size)), with_labels=True)
    print 'node drawing finished'
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    print 'edge drawing finished'
    plt.show()


# def run0():
#     WG = nx.read_gpickle(
#         '/Users/JerryHan88/PycharmProjects/taxi_projects/community_analysis/data/partitioned_group/2009-TH(30)-whole.pkl')
#     node_list = []
#     pos = nx.spring_layout(WG)
#     colors = ['c', 'm', 'y', 'r', 'b']
#     for x in range(1, 5):
#         SG = nx.read_gpickle('/Users/JerryHan88/PycharmProjects/taxi_projects/community_analysis/data/partitioned_group/2009-TH(30)-PD(%d).pkl' % x)
#         ns = SG.nodes()
#         node_list += ns
#         nx.draw_networkx_nodes(WG, pos, ns, node_size=2,
#                                node_color=colors[x], with_labels=True)
#     # nx.draw(G, nx.spring_layout(G))
#     nx.draw_networkx_edges(WG, pos, node_list, alpha=0.5)
#     plt.show()


if __name__ == '__main__':
    run()