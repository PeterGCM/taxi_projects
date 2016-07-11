import __init__
#
from c_individual_analysis.__init__ import ftd_stat_ap_both_fn, ftd_stat_ns_both_fn
from c_individual_analysis.__init__ import ftd_monthly_stats_ap_fn, ftd_monthly_stats_ns_fn
#
from taxi_common.file_handling_functions import remove_file, save_pickle_file
#
import csv
import pandas as pd


def run():
    for stat_both_fn, monthly_stats_fn in [(ftd_stat_ap_both_fn, ftd_monthly_stats_ap_fn),
                                           (ftd_stat_ns_both_fn, ftd_monthly_stats_ns_fn)]:
        remove_file(monthly_stats_fn)
        #
        df = pd.read_csv(stat_both_fn)
        # remove outlier
        column_names = df.columns.values[len(['yy','mm','did']):]
        for cn in column_names:
            df = df[((df[cn] - df[cn].mean()) / float(df[cn].std())).abs() < 3]
        df_gb = df.groupby(['yy', 'mm'])
        _data = [['yy', 'mm', 'num-drivers']]
        for v in df_gb.count().reset_index()[['yy', 'mm', 'did']].values:
            _data.append(list(v))
        for cn in column_names:
            _data[0] += ['%s-mean' % cn, '%s-sum' % cn, '%s-std' % cn]
            for i, x in enumerate(zip(df_gb.mean()[cn].values, df_gb.sum()[cn].values, df_gb.std()[cn].values)):
                _data[i+1] += x

        with open(monthly_stats_fn, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile)
            for row in _data:
                writer.writerow(row)

if __name__ == '__main__':
    run()
