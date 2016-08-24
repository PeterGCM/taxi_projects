import __init__
#
from community_analysis.__init__ import com_trip_dir
#
from taxi_common.file_handling_functions import check_dir_create
#
import pandas as pd
import csv


def run():
    target = '2009'
    ct_yyyy_dir = '%s/%s' % (com_trip_dir, target)
    ctrip_fn = '%s/%s-trip-community.csv' % (ct_yyyy_dir, target)
    #
    df = pd.read_csv(ctrip_fn)
    com_df = {}
    cn_names = set(df['cnum'])
    for cn in cn_names:
        com_df[cn] = df[(df['cnum'] == cn)]
    #
    zones_com_num = {}
    for cn, cdf in com_df.iteritems():
        cdf_gb = cdf.groupby(['si', 'sj'])
        for i, j, num in cdf_gb.count()['cnum'].to_frame('total-num-trip').reset_index().values:
            if not zones_com_num.has_key((i, j)):
                zones_com_num[(i, j)] = {}
            zones_com_num[(i, j)][cn] = num
    sl_summary_fn = '%s/%s_sl_summary.csv' % (ct_yyyy_dir, target)
    with open(sl_summary_fn, 'wt') as w_csvfile:
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
    #
    zones_com_num = {}
    for cn, cdf in com_df.iteritems():
        cdf_gb = cdf.groupby(['ei', 'ej'])
        for i, j, num in cdf_gb.count()['cnum'].to_frame('total-num-trip').reset_index().values:
            if not zones_com_num.has_key((i, j)):
                zones_com_num[(i, j)] = {}
            zones_com_num[(i, j)][cn] = num
    el_summary_fn = '%s/%s_el_summary.csv' % (ct_yyyy_dir, target)
    with open(el_summary_fn, 'wt') as w_csvfile:
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