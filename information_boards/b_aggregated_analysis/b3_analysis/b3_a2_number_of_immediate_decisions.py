import __init__
#
from information_boards.__init__ import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from information_boards.__init__ import charts_dir
from a_overall_analysis.__init__ import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn
#
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.charts import bar_table, one_pie_chart, two_pie_chart
#
import pandas as pd


def run():
    a2_dir = charts_dir + '/b_aggregated_a2 number of immediate decision'
    check_dir_create(a2_dir)
    for LABEL, label, fn in [('AP', 'ap', ap_tm_num_dur_fare_fn),
                             ('NS', 'ns', ns_tm_num_dur_fare_fn)]:
        whole_trips = pd.read_csv(fn)
        Y09 = whole_trips[(whole_trips['yy'] == 9)]
        Y10 = whole_trips[(whole_trips['yy'] == 10)]
        #
        Y09_gb, Y10_gb = Y09.groupby(['trip-mode']), Y10.groupby(['trip-mode'])
        Y09_tm_num, Y10_tm_num = Y09_gb.sum()['total-num'], Y10_gb.sum()['total-num']
        _data = [[int(Y09_tm_num[DIn_PIn]), int(Y10_tm_num[DIn_PIn])],
                 [int(Y09_tm_num[DIn_POut]), int(Y10_tm_num[DIn_POut])]]
        #
        row_labels, col_labels = ['Pick up in %s' % LABEL, 'Pick up out %s' % LABEL], ['Y2009', 'Y2010']
        bar_table((8,6), '', '', row_labels, col_labels, _data, a2_dir + '/table_decision_at_%s' % label)
        #
        per_data1 = [_data[1][0] / float(_data[0][0] + _data[1][0]), _data[0][0] / float(_data[0][0] + _data[1][0])]
        per_data2 = [_data[1][1] / float(_data[0][1] + _data[1][1]), _data[0][1] / float(_data[0][1] + _data[1][1])]
        one_pie_chart('', per_data1, ['Pick up out %s' % LABEL, 'Pick up in %s' % LABEL], a2_dir + '/Y2009_decision_at_%s' % label)
        one_pie_chart('', per_data2, ['Pick up out %s' % LABEL, 'Pick up in %s' % LABEL], a2_dir + '/Y2010_decision_at_%s' % label)
        #
        per_data1 = [_data[1][0] / float(_data[0][0] + _data[1][0]), _data[0][0] / float(_data[0][0] + _data[1][0])]
        per_data2 = [_data[1][1] / float(_data[0][1] + _data[1][1]), _data[0][1] / float(_data[0][1] + _data[1][1])]
        two_pie_chart(['Pick up out %s' % LABEL, 'Pick up in %s' % LABEL],
                      "Y2009", per_data1,
                      "Y2010", per_data2, a2_dir + '/decision_at_%s' % label)

if __name__ == '__main__':
    run()
