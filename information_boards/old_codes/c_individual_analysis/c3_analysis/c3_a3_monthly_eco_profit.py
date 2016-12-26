import __init__
#
from information_boards.__init__ import CENT, SEC3600
from information_boards.__init__ import charts_dir
from c_individual_analysis.__init__ import ftd_monthly_stats_ap_fn, ftd_monthly_stats_ns_fn
#
from taxi_common.file_handling_functions import remove_create_dir
from taxi_common.charts import multiple_line_chart
#
import pandas as pd


def run():
    a3_chart_dir = charts_dir + '/c_individual_a3 monthly economic profit'
    remove_create_dir(a3_chart_dir)
    #
    months = ['0901', '0902', '0903', '0904', '0905', '0906', '0907', '0908', '0909', '0910', '0911',
              '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1011', '1012']
    for label, monthly_stat_fn in [('ap', ftd_monthly_stats_ap_fn),
                                   ('ns', ftd_monthly_stats_ns_fn)]:
        Y09Y10_df = pd.read_csv(monthly_stat_fn)
        yss = []
        productivity_label = ['pin-eco-profit', 'pout-eco-profit']
        for l in productivity_label:
            yss.append((Y09Y10_df['%s-mean' % l] / float(CENT)).values)
        multiple_line_chart((15, 7.5), '', 'Year and Month', '$S', (months, 20), yss, productivity_label,
                            'upper left', a3_chart_dir + '/eco-profits-%s' % label)

if __name__ == '__main__':
    run()
