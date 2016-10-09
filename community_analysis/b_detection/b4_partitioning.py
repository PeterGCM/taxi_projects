import __init__
#
from community_analysis import dw_graph_dir, dw_graph_above_avg_prefix, dw_graph_above_per90_prefix
from community_analysis import group_dir, group_prepix
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, check_dir_create
from taxi_common.log_handling_functions import get_logger
#
import louvain
import igraph as ig

logger = get_logger('partitioning_95')


def run():
    check_dir_create(group_dir)
    #
    yyyy = '2009'
    #
    year_group_fpath = '%s/%s%s.pkl' % (group_dir, group_prepix, yyyy)
    if check_path_exist(year_group_fpath):
        return None
    logger.info('year dw graph loading')
    year_dw_graph1_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_above_per90_prefix, yyyy)
    year_dw_graph_above_avg = load_pickle_file(year_dw_graph1_fpath)
    num_edges = len(year_dw_graph_above_avg)
    logger.info('igraph generation total number of edges %d' % num_edges)
    igid, did_igid = 0, {}
    igG = ig.Graph(directed=True)
    for i, ((did0, did1), w) in enumerate(year_dw_graph_above_avg.iteritems()):
        if i % 1000 == 0:
            logger.info('processed %d edges' % i)
        if not did_igid.has_key(did0):
            igG.add_vertex(did0)
            did_igid[did0] = igid
            igid += 1
        if not did_igid.has_key(did1):
            igG.add_vertex(did1)
            did_igid[did1] = igid
            igid += 1
        igG.add_edge(did_igid[did0], did_igid[did1], weight=w)
    logger.info('Partitioning')
    part = louvain.find_partition(igG, method='Modularity', weight='weight')
    logger.info('Whole group pickling')
    part.graph.write_pickle(year_group_fpath)
    logger.info('Each group pickling')
    for i, sg in enumerate(part.subgraphs()):
        year_a_group_fpath = '%s/%s%s-G(%d).pkl' % (group_dir, group_prepix, yyyy, i)
        sg.write_pickle(year_a_group_fpath)


if __name__ == '__main__':
    run()





# import louvain
# import igraph as ig
#
#
# l = [("a", "b", 3.0), ("c", "d", 4.0), ("a", "c", 5.0)]
#
#
# vertices = [100 +i for i in range(10)]
# edges = [(0,2),(0,1),(0,3),
#          (1,0),(1,2),(1,3),
#          (2,0),(2,1),(2,3),
#          (3,0),(3,1),(3,2),
#          (2,4),(4,5),(4,6),(5,4),(5,6),(6,4),(6,7),
#          (8,9)
#          ]
#
# g = ig.Graph(vertex_attrs={"label": vertices}, edges=edges, directed=True, edge_attrs={"weight": range(len(edges))})
#
# for e in g.es:
#     print g.vs[e.source]['label'], g.vs[e.target]['label'], e['weight']
#
#
#
# for v in g.vs:
#     print v['label'], '-', 'S(%d)' % len(g.neighbors(v, mode="out")),
#     for i in g.neighbors(v, mode="out"):
#         print g.vs[i]['label'],
#     print ''
#
# print g.is_weighted()
#
# print ''
# part = louvain.find_partition(g, method='Modularity', weight='weight')
# # print part.graph
# for sg in part.subgraphs():
#     for v in sg.vs:
#         print v['label'],
#     # print sg.vs[0].attributes()
#     print sg
#     print