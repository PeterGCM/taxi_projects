import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import driversRelations_fpaths
#
from taxi_common.file_handling_functions import load_pickle_file
#
import igraph as ig
#

tm, year = 'spendingTime', '2012'
gp_dpath = dpaths[tm, year, 'groupPartition']
gp_prefix = prefixs[tm, year, 'groupPartition']

gp_fpath = '%s/%sG(20).pkl' % (gp_dpath, gp_prefix)
igG = ig.Graph.Read_Pickle(gp_fpath)


driversRelations = load_pickle_file(driversRelations_fpaths[year])
whole_drivers = driversRelations.keys()


# igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn))
groupDrivers = set()
for e in igG.es:
    did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
    groupDrivers.add(did0)
    groupDrivers.add(did1)