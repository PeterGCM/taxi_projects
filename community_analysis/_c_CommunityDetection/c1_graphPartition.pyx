import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, load_pickle_file, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import csv
import louvain
import numpy as np
import igraph as ig

logger = get_logger()

sig_level = 0.01

year = '20%02d' % 9
depVar = 'roamingTime'
# depVar = 'interTravelTime'
#
#
if_dpath = dpaths[depVar, 'influenceGraph']
if_prefixs = prefixs[depVar, 'influenceGraph']
of_dpath = dpaths[depVar, 'graphPartition']
of_prefixs = prefixs[depVar, 'graphPartition']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run():
    comSummary_fpath = '%s/%s%s-summary.csv' % (of_dpath, of_prefixs, year)
    originalGraph_fpath = '%s/%s%s-original.pkl' % (of_dpath, of_prefixs, year)
    comDrivers_fpath = '%s/%s%s-drivers.pkl' % (of_dpath, of_prefixs, year)
    #
    with open(comSummary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(
            ['comName',
             'numDrivers', 'numRelations', 'graphComplexity',
             'weightMedian', 'weightMean', 'weightStd',
             'tieStrength', 'contribution', 'benCon'])
    #
    logger.info('Start handling %s' % depVar)
    orignal_graph = {}
    for fn in get_all_files(if_dpath, '%s%s*' % (if_prefixs, year)):
        regression_graph = load_pickle_file('%s/%s' % (if_dpath, fn))
        for i, ((did0, did1), (_, pv, w)) in enumerate(regression_graph.iteritems()):
            if pv > sig_level:
                continue
            orignal_graph[did0, did1] = w
    save_pickle_file(originalGraph_fpath, orignal_graph)
    #
    igid, did_igid = 0, {}
    igG = ig.Graph(directed=True)
    for i, ((did0, did1), w) in enumerate(orignal_graph.iteritems()):
        if not did_igid.has_key(did0):
            igG.add_vertex(did0)
            did_igid[did0] = igid
            igid += 1
        if not did_igid.has_key(did1):
            igG.add_vertex(did1)
            did_igid[did1] = igid
            igid += 1
        igG.add_edge(did_igid[did0], did_igid[did1], weight=abs(w))
    #
    logger.info('Partitioning')
    part = louvain.find_partition(igG, method='Modularity', weight='weight')
    logger.info('Each community graph pickling and summary')
    comDrivers = {}
    for i, sg in enumerate(part.subgraphs()):
        cn = 'C(%d)' % i
        comGraph_fpath = '%s/%s%s-%s.pkl' % (of_dpath, of_prefixs, year, cn)
        sg.write_pickle(comGraph_fpath)
        #
        nodes = [v['name'] for v in sg.vs]
        weights = [e['weight'] for e in sg.es]
        numDrivers = len(nodes)
        numRelations = len(weights)
        graphComplexity = numRelations / float(numDrivers)
        weights_np = np.asarray(weights)
        weightMedian = np.median(weights_np)
        weightMean = np.mean(weights_np)
        weightStd = np.std(weights_np)
        tieStrength = weights_np.sum() / float(numDrivers)
        contribution = weights_np.sum() / float(numRelations)
        benCon = tieStrength / float(numDrivers)
        with open(comSummary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [
                cn,
                numDrivers, numRelations, graphComplexity,
                weightMedian, weightMean, weightStd,
                tieStrength, contribution, benCon
            ]
            writer.writerow(new_row)
        img_fpath = '%s/%simg-%s-%s.pdf' % (of_dpath, of_prefixs, year, cn)
        layout = sg.layout("kk")
        if len(nodes) < 100:
            ig.plot(sg, img_fpath, layout=layout, vertex_label=nodes, vertex_color='white')
        else:
            ig.plot(sg, img_fpath, layout=layout, vertex_color='white')
        comDrivers[cn] = nodes
        coef_fpath = '%s/%scoef-%s-%s.csv' % (of_dpath, of_prefixs, year, cn)
        with open(coef_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['groupName', 'did0', 'did1', 'coef'])
            for e in sg.es:
                did0, did1 = [sg.vs[nIndex]['name'] for nIndex in e.tuple]
                coef = e['weight']
                writer.writerow([cn, did0, did1, coef])
    save_pickle_file(comDrivers_fpath, comDrivers)


if __name__ == '__main__':
    run()

