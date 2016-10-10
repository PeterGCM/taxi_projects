import __init__
#
from community_analysis import group_dir
#
import igraph as ig
#

for i in range(4):
    pkl_fn = 'group-per99-2009-M01M02M03-G(%d).pkl' % i
    pkl_fpath = '%s/%s' % (group_dir, pkl_fn)


    igG = ig.Graph.Read_Pickle(pkl_fpath)
    print len(igG.vs)
    print type(igG)