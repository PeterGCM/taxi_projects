import __init__
#
from information_boards.__init__ import tables_dir
from c_individual_analysis.__init__ import ftd_stat_ap_both_fn, ftd_stat_ns_both_fn
from c_individual_analysis.__init__ import ftd_monthly_stats_ap_fn, ftd_monthly_stats_ns_fn
#
from taxi_common.file_handling_functions import remove_create_dir, write_text_file
#
import csv
import pandas as pd
import numpy as np
import scipy.stats as stats
from prettytable import PrettyTable


def run():
    a1_table_dir = tables_dir + '/c_individual_a1 both year t test'
    remove_create_dir(a1_table_dir)
    #
    for label, stat_both_fn, monthly_stat_fn in [('ap', ftd_stat_ap_both_fn, ftd_monthly_stats_ap_fn),
                                                 ('ns', ftd_stat_ns_both_fn, ftd_monthly_stats_ns_fn)]:
        headers = None
        with open(stat_both_fn, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
        column_names = headers[len(['yy', 'mm', 'did']):]
        Y09Y10_df = pd.read_csv(monthly_stat_fn)
        Y09_df, Y10_df = Y09Y10_df[(Y09Y10_df['yy'] == 9)], Y09Y10_df[(Y09Y10_df['yy'] == 10)]
        #
        _table = PrettyTable(['Measeure', 'Diff.',
                                          'Y2010', 'Y2009', 't-statistic', 'p-value'])
        _table.align['Measeure'] = 'l'
        for l in ['Measeure', 'Diff.', 'Y2010', 'Y2009', 't-statistic', 'p-value']:
            _table.align[l] = 'r'

        for cn in column_names:
            Y10_values, Y09_values = Y10_df[cn + '-mean'], Y09_df[cn + '-mean']
            Y10_mean, Y09_mean = np.mean(Y10_values), np.mean(Y09_values)
            t_stats, p_value = stats.ttest_ind(Y10_values, Y09_values)
            _table.add_row([cn, Y10_mean - Y09_mean,
                            Y10_mean, Y09_mean, t_stats, p_value])
        write_text_file(a1_table_dir + '/t-test-%s' % label, _table.get_string(), is_first=True)


if __name__ == '__main__':
    run()
