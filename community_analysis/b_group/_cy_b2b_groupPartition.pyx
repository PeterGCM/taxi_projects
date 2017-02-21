import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, load_pickle_file, save_pickle_file, check_path_exist
from taxi_common.log_handling_functions import get_logger
#
import csv
import louvain
import igraph as ig
import numpy as np

logger = get_logger()


def run():
    cg_dpath = dpaths['baseline', '2009', 'countGraph']
    cg_prefix = prefixs['baseline', '2009', 'countGraph']
    gp_dpath = dpaths['baseline', '2009', 'groupPartition']
    gp_prefix = prefixs['baseline', '2009', 'groupPartition']
    #
    check_dir_create(gp_dpath)
    #
    gp_summary_fpath = '%s/%ssummary.csv' % (gp_dpath, gp_prefix)
    gp_original_fpath = '%s/%soriginal.pkl' % (gp_dpath, gp_prefix)
    gp_drivers_fpath = '%s/%sdrivers.pkl' % (gp_dpath, gp_prefix)
    #
    with open(gp_summary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['groupName', 'numDrivers', 'numRelations', 'graphComplexity', 'tieStrength', 'contribution', 'benCon'])
    #
    logger.info('Start handling SP_group_dpath')
    if not check_path_exist(gp_original_fpath):
        original_graph = {}
        weights = []
        for fn in get_all_files(cg_dpath, '%s*' % cg_prefix):
            count_graph = load_pickle_file('%s/%s' % (cg_dpath, fn))
            logger.info('Start handling; %s' % fn)
            numEdges = len(count_graph)
            moduloNumber = numEdges / 5
            for i, ((did0, did1), w) in enumerate(count_graph.iteritems()):
                # if w < 253.0: # 95 percentile value
                #     continue
                if i % moduloNumber == 0:
                    logger.info('Handling; %.2f' % (i / float(numEdges)))
                original_graph[did0, did1] = w
                weights += [w]
        logger.info('pickling')
        numEdges = len(original_graph)
        moduloNumber = numEdges / 100
        originalFiltered_graph = {}
        #
        weights_np = np.asarray(weights)
        th = 99
        thValue = np.percentile(weights_np, th)
        logger.info('------------------------------------------')
        logger.info('# of edges: %d' % len(weights))
        logger.info('%d percentile value: %f' % (th, thValue))
        logger.info('------------------------------------------')
        numRemovedEdges = 0
        for i, ((did0, did1), w) in enumerate(original_graph.iteritems()):
            if i % moduloNumber == 0:
                logger.info('Handling; %.2f' % (i / float(numEdges)))
            if w < thValue:
                numRemovedEdges += 1
                continue
            originalFiltered_graph[did0, did1] = w
        logger.info('------------------------------------------')
        logger.info('# of removed edges: %d' % numRemovedEdges)
        logger.info('------------------------------------------')
        save_pickle_file(gp_original_fpath, originalFiltered_graph)
    else:
        originalFiltered_graph = load_pickle_file(gp_original_fpath)
    #
    logger.info('igraph converting')
    igid, did_igid = 0, {}
    igG = ig.Graph(directed=True)
    numEdges = len(originalFiltered_graph)
    print numEdges, np.percentile(originalFiltered_graph.values(), 95)
    moduloNumber = numEdges / 10
    for i, ((did0, did1), w) in enumerate(originalFiltered_graph.iteritems()):
        if w < 500.0:
            continue
        if i % moduloNumber == 0:
            logger.info('Handling; %.2f' % (i / float(numEdges)))
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
    logger.info('Each group pickling and summary')
    gn_drivers = {}
    for i, sg in enumerate(part.subgraphs()):
        gn = 'G(%d)' % i
        group_fpath = '%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn)
        sg.write_pickle(group_fpath)
        #
        drivers = [v['name'] for v in sg.vs]
        weights = [e['weight'] for e in sg.es]
        graphComplexity = len(weights) / float(len(drivers))
        tie_strength = sum(weights) / float(len(drivers))
        contribution = sum(weights) / float(len(weights))
        benCon = tie_strength / float(len(drivers))
        with open(gp_summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([gn, len(drivers), len(weights), graphComplexity, tie_strength, contribution, benCon])
        gl_img_fpath = '%s/%simg-%s.pdf' % (gp_dpath, gp_prefix, gn)
        layout = sg.layout("kk")
        if len(drivers) < 100:
            ig.plot(sg, gl_img_fpath, layout=layout, vertex_label=drivers, vertex_color='white')
        else:
            ig.plot(sg, gl_img_fpath, layout=layout, vertex_color='white')
        gn_drivers[gn] = drivers
        # gc_fpath = '%s/%scoef-%s.csv' % (gp_dpath, gp_prefix, gn)
        # with open(gc_fpath, 'wt') as w_csvfile:
        #     writer = csv.writer(w_csvfile, lineterminator='\n')
        #     writer.writerow(['groupName', 'did0', 'did1', 'coef'])
        #     for e in sg.es:
        #         did0, did1 = [sg.vs[nIndex]['name'] for nIndex in e.tuple]
        #         coef = e['weight']
        #         writer.writerow([gn, did0, did1, coef])
    save_pickle_file(gp_drivers_fpath, gn_drivers)


if __name__ == '__main__':
    run()

