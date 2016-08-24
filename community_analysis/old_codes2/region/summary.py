import __init__
#
from community_analysis.__init__ import com_log_dir
#
from taxi_common.file_handling_functions import check_dir_create
#
import pandas as pd
import csv


def run():
    target = '2009'
    cl_yyyy_dir = '%s/%s' % (com_log_dir, target); check_dir_create(cl_yyyy_dir)
    com_log_fn = '%s/%s-log-community.csv' % (cl_yyyy_dir, target)
    #
    df = pd.read_csv(com_log_fn)
    com_df = {}
    cn_names = set(df['community'])
    for cn in cn_names:
        com_df[cn] = df[(df['community'] == cn)]
    zones_com_num = {}
    for cn, cdf in com_df.iteritems():
        cdf_gb = cdf.groupby(['i', 'j'])
        for i, j, num in cdf_gb.count()['community'].to_frame('total-num-trip').reset_index().values:
            if not zones_com_num.has_key((i, j)):
                zones_com_num[(i, j)] = {}
            zones_com_num[(i, j)][cn] = num

    summary_fn = '%s/%s_region_summary.csv' % (cl_yyyy_dir, target)
    with open(summary_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['(i, j)'] + list(cn_names)
        writer.writerow(new_headers)
        for k in sorted(zones_com_num.keys()):
            cn_num = zones_com_num[k]
            row = [k]
            for cn in cn_num:
                if cn_num.has_key(cn):
                    row.append(cn_num[cn])
                else:
                    row.append(0)
            writer.writerow(row)


if __name__ == '__main__':
    run()