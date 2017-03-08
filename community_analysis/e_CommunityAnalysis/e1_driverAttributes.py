import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import taxi_data
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
#
import pandas as pd
import igraph as ig
import csv


demo_dpath = '%s/%s' % (taxi_data, 'demographics')
demo_fpath = '%s/driver-data.csv' % demo_dpath

tm, year = 'spendingTime', '2009'
gp_dpath = dpaths[tm, year, 'groupPartition']
gp_prefix = prefixs[tm, year, 'groupPartition']
gp_summary_fpath = '%s/%ssummary.csv' % (gp_dpath, gp_prefix)
#
gs_df = pd.read_csv(gp_summary_fpath)
for i, gn in enumerate(gs_df['groupName'].values):
    igG = ig.Graph.Read_Pickle('%s/%s%s.pkl' % (gp_dpath, gp_prefix, gn))
    groupDrivers = set()
    for e in igG.es:
        did0, did1 = [igG.vs[nIndex]['name'] for nIndex in e.tuple]
        groupDrivers.add(did0)
        groupDrivers.add(did1)
    demoGroup_fpath = '%s/%s.csv' % (demo_dpath, gn)
    print demo_fpath
    with open(demo_fpath, 'rU') as r_csvfile:
        reader = csv.reader(r_csvfile)
        header = reader.next()
        hid = {h: i for i, h in enumerate(header)}
        with open(demoGroup_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(header)
            for row in reader:
                did = int(row[hid['id']])
                if did in groupDrivers:
                    writer.writerow(row)
