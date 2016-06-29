from graph_tool.all import *
import numpy as np

def run(did_relations):
    #
    # Filtering and edges' weight arrangement
    #
    edge_weight = {}
    for _did0, relations in did_relations:
        assert False
        nums = [num for num in relations.itervalues()]
        nums_avg, num_std = np.mean(nums), np.std(nums)
        for _did1, num_relations in relations.iteritems():
            if num_relations < nums_avg + num_std:
                continue
            did0, did1 = int(_did0), int(_did1)
            if did0 > did1:
                did0, did1 = int(_did1), int(_did0)
            if not edge_weight.key_has((did0, did1)):
                edge_weight[(did0, did1)] = 0
            edge_weight[(did0, did1)] += num_relations  
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
    graph_draw(g, output_size=(1200, 1200), output="new.pdf")
#     for i, lo in enumerate([sfdp_layout(g), arf_layout(g, max_iter=0),
#                           radial_tree_layout(g, g.vertex(0)),
#                           fruchterman_reingold_layout(g, n_iter=1000)]):
#         graph_draw(g, pos=lo, output_size=(1200, 1200), output="lo%d.pdf" % i)
