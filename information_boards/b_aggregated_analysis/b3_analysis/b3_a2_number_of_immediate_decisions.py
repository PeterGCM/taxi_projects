import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from a_overall_analysis import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn
#
from taxi_common.charts import bar_table, one_pie_chart, two_pie_chart
#
import pandas as pd
#
def run():
    for LABEL, label, fn in [('AP', 'ap', ap_tm_num_dur_fare_fn),
                             ('NS', 'ns', ns_tm_num_dur_fare_fn)]:
        whole_trips = pd.read_csv(fn)
        Y09 = whole_trips[(whole_trips['yy'] == 9)]
        Y10 = whole_trips[(whole_trips['yy'] == 10)]
        #
        Y09_gb, Y10_gb = Y09.groupby(['trip-mode']), Y10.groupby(['trip-mode'])
        Y09_tm_num, Y10_tm_num = Y09_gb.sum()['num-tm'], Y10_gb.sum()['num-tm']
        _data = [[Y09_tm_num[DIn_PIn], Y10_tm_num[DIn_PIn]],
                 [Y09_tm_num[DIn_POut], Y10_tm_num[DIn_POut]]]
        #
        row_labels, col_labels = ['Pick up in %s' % LABEL, 'Pick up out %s' % LABEL], ['Y2009', 'Y2010']
        bar_table("", '', row_labels, col_labels, _data, 'Driver_decision_at_%s' % label)
        #
        per_data1 = [_data[1][0] / (_data[0][0] + _data[1][0]), _data[0][0] / (_data[0][0] + _data[1][0])]
        per_data2 = [_data[1][1] / (_data[0][1] + _data[1][1]), _data[0][1] / (_data[0][1] + _data[1][1])]
        one_pie_chart('', per_data1, ['Pick up out %s' % LABEL, 'Pick up in %s' % LABEL], 'Y2009_decision_at_%s' % label)
        one_pie_chart('', per_data2, ['Pick up out %s' % LABEL, 'Pick up in %s' % LABEL], 'Y2010_decision_at_%s' % label)
        #
        per_data1 = [_data[1][0] / (_data[0][0] + _data[1][0]), _data[0][0] / (_data[0][0] + _data[1][0])]
        per_data2 = [_data[1][1] / (_data[0][1] + _data[1][1]), _data[0][1] / (_data[0][1] + _data[1][1])]
        two_pie_chart(['Pick up out %s' % LABEL, 'Pick up in %s' % LABEL],
                      "Y2009", per_data1,
                      "Y2010", per_data2, 'decision_at_%s' % label)

if __name__ == '__main__':
    run()
