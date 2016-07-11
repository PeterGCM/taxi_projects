import __init__
#
from c_individual_analysis.__init__ import ftd_Y09_stat_ap_fn, ftd_Y10_stat_ap_fn
from c_individual_analysis.__init__ import ftd_Y09_stat_ns_fn, ftd_Y10_stat_ns_fn
from c_individual_analysis.__init__ import ftd_driver_stats_ap_fn, ftd_driver_stats_ns_fn
#
from taxi_common.file_handling_functions import remove_file, save_pickle_file
#
import csv
import pandas as pd

def run():
    for Y09_stat_fn, Y10_stat_fn, driver_stats_fn in [(ftd_Y09_stat_ap_fn, ftd_Y10_stat_ap_fn, ftd_driver_stats_ap_fn), 
                            (ftd_Y09_stat_ns_fn, ftd_Y10_stat_ns_fn, ftd_driver_stats_ns_fn)]:
        remove_file(driver_stats_fn)
        Y09_df, Y10_df = pd.read_csv(Y09_stat_fn), pd.read_csv(Y10_stat_fn)
        # remove outlier
        column_names = Y09_df.columns.values[len(['yy','mm','did']):]
        for cn in column_names:
            Y09_df = Y09_df[((Y09_df[cn] - Y09_df[cn].mean()) / float(Y09_df[cn].std())).abs() < 3]
            Y10_df = Y10_df[((Y10_df[cn] - Y10_df[cn].mean()) / float(Y10_df[cn].std())).abs() < 3]
        _data = [['did']]
        both_year_ftd = set(Y09_df['did']).intersection(set(Y10_df['did']))
        for cn in column_names:
            _data[0] += ['Diff-%s' % cn,
                         'Y10-%s-mean' % cn, 'Y09-%s-mean' % cn,
                         'Y10-%s-sum' % cn, 'Y09-%s-sum' % cn,
                         'Y10-%s-std' % cn, 'Y09-%s-std' % cn]
        print len(both_year_ftd)
        for i, did in enumerate(both_year_ftd):
            Y09_did_df, Y10_did_df = Y09_df[(Y09_df['did'] == did)], Y10_df[(Y10_df['did'] == did)]
            Y09_did_gb, Y10_did_gb = Y09_did_df.groupby(['did']), Y10_did_df.groupby(['did'])
            _data.append([did])
            for j, cn in enumerate(column_names):
                for x in zip(Y10_did_gb.mean()[cn].values - Y09_did_gb.mean()[cn].values,
                             Y10_did_gb.mean()[cn].values, Y09_did_gb.mean()[cn].values,
                             Y10_did_gb.sum()[cn].values, Y09_did_gb.sum()[cn].values,
                             Y10_did_gb.std()[cn].values, Y09_did_gb.std()[cn].values):
                    _data[-1] += x
            if i % 100 == 0:
                print '%d,' % i,
        #
        with open(driver_stats_fn, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            for row in _data:
                writer.writerow(row)
        print ''

if __name__ == '__main__':
    run()
