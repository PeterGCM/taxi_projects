import __init__

from graph_tool.all import *
import numpy as np
from taxi_common.file_handling_functions import load_pickle_file

def run():
    # TODO
    # Decide how many days will you consider
    # Get the maximum weight
    # Draw graphs by changing a threshold value about the minimum condition for weights
    #     the maximum weight * [0.8, 0.4, 0.2]

    print 'start loading'
    edge_weight = load_pickle_file('/Users/JerryHan88/PycharmProjects/taxi_projects/community_detection/data/edge/_0901/20090101.pkl')
    max_weight = max([v for v in edge_weight.itervalues()])
    filtered_ew = {}
    print 'start filtering'
    for k, v in edge_weight.iteritems():
        if v < max_weight * 0.8:
            continue
        filtered_ew[k] = v
    #
    # Generate a graph
    #
    g = Graph()
    g.edge_properties["weight"] = g.new_edge_property("int")
    did_index, index_did = {}, {}
    num_drivers = 0
    for (did0, did1), num_relations in filtered_ew.iteritems():
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
    print 'start drawing graph'
    graph_draw(g, output_size=(1200, 1200), output="filtered.pdf")


    # graph_draw(g, pos=fruchterman_reingold_layout(g, n_iter=1000), output_size=(1200, 1200), output="lo_fruchter.pdf")


    # for i, lo in enumerate([# sfdp_layout(g),
    #                         arf_layout(g, max_iter=0),
    #                       radial_tree_layout(g, g.vertex(0)),
    #                       fruchterman_reingold_layout(g, n_iter=1000)]):

    #     print i
    #     graph_draw(g, pos=lo, output_size=(1200, 1200), output="lo%d.pdf" % i)


if __name__ == '__main__':
    run()