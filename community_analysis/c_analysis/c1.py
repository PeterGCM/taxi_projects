import __init__
#
from community_analysis import group_dir
#
import igraph as ig
#
month3_group = {}
for month3 in ['M01M02M03', 'M02M03M04']:
    for i in range(4):
        pkl_fn = 'group-per99-2009-%s-G(%d).pkl' % i
        pkl_fpath = '%s/%s' % (group_dir, pkl_fn)
        igG = ig.Graph.Read_Pickle(pkl_fpath)
        month3_group[month3, i] = [v['name'] for v in igG.vs]
whole_drivers = list(set(month3_group.values()))

for