import __init__

from graph_tool.all import *
import numpy as np
from taxi_common.file_handling_functions import load_pickle_file

def run():
    #
    # Filtering and edges' weight arrangement
    #
    edge_weight = load_pickle_file('/Users/JerryHan88/taxi_data/community_data/linkage/20090101-20090110/ft_20090101.pkl')



    #
    # Generate a graph
    #
    g = Graph()
    g.edge_properties["weight"] = g.new_edge_property("int")
    did_index, index_did = {}, {}
    num_drivers = 0
    for (did0, did1), num_relations in edge_weight.iteritems():
        if did0 not in did_index:
            did_index[did0] = num_drivers
            index_did[num_drivers] = did0
            g.add_vertex()
            num_drivers += 1
        if did1 not in did_index:
            did_index[did1] = num_drivers
            index_did[num_drivers] = did1
            g.add_vertex()
            num_drivers += 1
        v0, v1 = g.vertex(did_index[did0]), g.vertex(did_index[did1])
        e = g.add_edge(v0, v1)
        g.ep.weight[e] = num_relations
    # graph_draw(g, output_size=(1200, 1200), output="new.pdf")
    print 'start'

    graph_draw(g, pos=fruchterman_reingold_layout(g, n_iter=1000), output_size=(1200, 1200), output="lo_fruchter.pdf")


    # for i, lo in enumerate([# sfdp_layout(g),
    #                         arf_layout(g, max_iter=0),
    #                       radial_tree_layout(g, g.vertex(0)),
    #                       fruchterman_reingold_layout(g, n_iter=1000)]):

    #     print i
    #     graph_draw(g, pos=lo, output_size=(1200, 1200), output="lo%d.pdf" % i)


if __name__ == '__main__':
    run()