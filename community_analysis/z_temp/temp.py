import __init__
import community_analysis
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import load_pickle_file
if_dpath = dpaths['roamingTime', 'priorPresence']
if_prefix = prefixs['roamingTime', 'priorPresence']
year = 2009
did1 = 37384
did0 = 9925
fpath = '%s/%s%d-%d.csv' % (if_dpath, if_prefix, year, did1)
df = pd.read_csv(fpath)

_did0 = '%d' % did0
df[(df[_did0] == 1)][['month', 'day', 'hour', _did0, 'zi', 'zj']]