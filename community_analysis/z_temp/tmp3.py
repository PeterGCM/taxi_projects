import __init__
'''
'''

from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import get_all_files, load_pickle_file

year = '20%02d' % 9
# depVar = 'roamingTime'
depVar = 'interTravelTime'
#
#
of_dpath = dpaths[depVar, 'influenceGraph']
of_prefixs = prefixs[depVar, 'influenceGraph']


countRelationWhole = {k: 0 for k in ['sigPos', 'sigNeg', 'XsigPos', 'XsigNeg']}

for fn in get_all_files(of_dpath, '%scount-*' % of_prefixs):
    print fpath
    fpath = '%s/%s' % (of_dpath, fn)
    countRelation = load_pickle_file(fpath)
    for n in ['sigPos', 'sigNeg', 'XsigPos', 'XsigNeg']:
        countRelationWhole[n] += countRelation[n]

print countRelationWhole

