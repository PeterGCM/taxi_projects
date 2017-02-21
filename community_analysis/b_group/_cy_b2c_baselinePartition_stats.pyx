import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, load_pickle_file, save_pickle_file
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import pandas as pd
import igraph as ig
import numpy as np

logger = get_logger()


def run():
    tm, year = 'spendingTime', '2009'
    gp_dpath = dpaths[tm, year, 'groupPartition']
    gp_prefix = prefixs[tm, year, 'groupPartition']
    gp_original_fpath = '%s/%soriginal.pkl' % (gp_dpath, gp_prefix)
    orignal_graph = load_pickle_file(gp_original_fpath)
    #
    tm, year = 'baseline', '2009'
    gp_dpath = dpaths[tm, year, 'groupPartition']
    gp_prefix = prefixs[tm, year, 'groupPartition']
    gpBaseline_summary_fpath = '%s/%ssummary.csv' % (gp_dpath, gp_prefix)
    gpBaseline_summary_new_fpath = '%s/%ssummary__.csv' % (gp_dpath, gp_prefix)
    #
    with open(gpBaseline_summary_new_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(
            ['groupName',
             'numDrivers', 'numRelations', 'graphComplexity',
             'weightMedian', 'weightMean', 'weightStd',
             'tieStrength', 'contribution', 'benCon'])
    #
    gs_df = pd.read_csv(gpBaseline_summary_fpath)
    for i, gn in enumerate(gs_df['groupName'].values):
        nodes = set()
        weights = []
        igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn))
        for e in igG.es:
            did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
            nodes.add(did0)
            nodes.add(did1)
            k = (did0, did1)
            if orignal_graph.has_key(k):
                weights += [abs(orignal_graph[k])]
            else:
                weights += [0]
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

        with open(gpBaseline_summary_new_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [
                gn,
                numDrivers,numRelations, graphComplexity,
                weightMedian, weightMean, weightStd,
                tieStrength, contribution, benCon
            ]
            writer.writerow(new_row)

if __name__ == '__main__':
    run()

