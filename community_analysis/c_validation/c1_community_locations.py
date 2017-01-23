import __init__
#
'''

'''
#
from community_analysis import SP_group_summary_fpath, RP_group_summary_fpath
#
import pandas as pd

df = pd.read_csv(SP_group_summary_fpath)


df =  df.sort_values(by='contribution',ascending=False)
print df.head(5)['groupName']


# use percentile values!! for selecting groups and drivers