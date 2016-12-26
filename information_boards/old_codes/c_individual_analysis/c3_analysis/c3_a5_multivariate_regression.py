import __init__
#
from information_boards.__init__ import tables_dir
from c_individual_analysis.__init__ import ftd_driver_stats_ap_fn, ftd_driver_stats_ns_fn
#
from taxi_common.file_handling_functions import check_dir_create
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sys


def run():
    a5_table_dir = tables_dir + '/c_individual_a5 multivariate regression'
    check_dir_create(a5_table_dir)

    for loc, stat_fn in [('ap', ftd_driver_stats_ap_fn),
                         ('ns', ftd_driver_stats_ns_fn)]:
        sys.stdout = open('%s/%s' % (a5_table_dir, 'mr-%s.txt'% loc), 'w')
        df = pd.read_csv(stat_fn)
        diff_df_cn = [cn for cn in df.columns.values if cn.startswith('diff')]
        diff_df = df[diff_df_cn]
        for i, cn in enumerate(diff_df_cn):
            other_cns = diff_df_cn[:]; other_cns.pop(i)
            fomula = '%s ~ '%cn + ' + '.join(other_cns)
            est = smf.ols(fomula, data=diff_df).fit()
            print est.summary()


if __name__ == '__main__':
    run()
