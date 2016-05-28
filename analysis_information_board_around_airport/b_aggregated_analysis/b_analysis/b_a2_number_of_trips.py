from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn
from supports._setting import DInAP_PInAP, DInAP_POutAP
from supports._setting import DInNS_PInNS, DInNS_POutNS
from supports.charts import bar_table, one_pie_chart, two_pie_chart
#
import pandas as pd
#
def run():
    ap_analysis()
    ns_analysis()

def ap_analysis():
    whole_trips = pd.read_csv(ap_tm_num_dur_fare_fn)
    Y09 = whole_trips[(whole_trips['yy'] == 9)]
    Y10 = whole_trips[(whole_trips['yy'] == 10)]
    #
    Y09_gb, Y10_gb = Y09.groupby(['ap-trip-mode']), Y10.groupby(['ap-trip-mode'])
    Y09_tm_num, Y10_tm_num = Y09_gb.sum()['num-tm'], Y10_gb.sum()['num-tm']
    _data = [[Y09_tm_num[DInAP_PInAP], Y10_tm_num[DInAP_PInAP]],
             [Y09_tm_num[DInAP_POutAP], Y10_tm_num[DInAP_POutAP]]]
    #
    row_labels, col_labels = ['Pick up in AP', 'Pick up out AP'], ['Y2009', 'Y2010']
    bar_table("", '', row_labels, col_labels, _data, 'Driver_decision_at_ap')
    #
    per_data1 = [_data[1][0] / (_data[0][0] + _data[1][0]), _data[0][0] / (_data[0][0] + _data[1][0])]
    per_data2 = [_data[1][1] / (_data[0][1] + _data[1][1]), _data[0][1] / (_data[0][1] + _data[1][1])]
    one_pie_chart('', per_data1, ['Pick up out AP', 'Pick up in AP'], 'Y2009_decision_at_ap')
    one_pie_chart('', per_data2, ['Pick up out AP', 'Pick up in AP'], 'Y2010_decision_at_ap')
    #
    per_data1 = [_data[1][0] / (_data[0][0] + _data[1][0]), _data[0][0] / (_data[0][0] + _data[1][0])]
    per_data2 = [_data[1][1] / (_data[0][1] + _data[1][1]), _data[0][1] / (_data[0][1] + _data[1][1])]
    two_pie_chart(['Pick up out AP', 'Pick up in AP'],
                  "Y2009", per_data1,
                  "Y2010", per_data2, 'decision_at_ap')

def ns_analysis():
    whole_trips = pd.read_csv(ns_tm_num_dur_fare_fn)
    Y09 = whole_trips[(whole_trips['yy'] == 9)]
    Y10 = whole_trips[(whole_trips['yy'] == 10)]
    #
    Y09_gb, Y10_gb = Y09.groupby(['ns-trip-mode']), Y10.groupby(['ns-trip-mode'])
    Y09_tm_num, Y10_tm_num = Y09_gb.sum()['num-tm'], Y10_gb.sum()['num-tm']
    _data = [[ Y09_tm_num[DInNS_PInNS], Y10_tm_num[DInNS_PInNS]],
            [ Y09_tm_num[DInNS_POutNS], Y10_tm_num[DInNS_POutNS]]]
    #
    row_labels, col_labels = ['Pick up in NS', 'Pick up out NS'], ['Y2009', 'Y2010']
    bar_table("", '', row_labels, col_labels, _data, 'Driver_decision_at_ns')
    #
    per_data1 = [_data[1][0] / (_data[0][0] + _data[1][0]), _data[0][0] / (_data[0][0] + _data[1][0])]
    per_data2 = [_data[1][1] / (_data[0][1] + _data[1][1]), _data[0][1] / (_data[0][1] + _data[1][1])]
    one_pie_chart('', per_data1, ['Pick up out NS', 'Pick up in NS'], 'Y2009_decision_at_ns')
    one_pie_chart('', per_data2, ['Pick up out NS', 'Pick up in NS'], 'Y2010_decision_at_ns')
    #
    per_data1 = [_data[1][0] / (_data[0][0] + _data[1][0]), _data[0][0] / (_data[0][0] + _data[1][0])]
    per_data2 = [_data[1][1] / (_data[0][1] + _data[1][1]), _data[0][1] / (_data[0][1] + _data[1][1])]
    two_pie_chart(['Pick up out NS', 'Pick up in NS'],
                  "Y2009", per_data1,
                  "Y2010", per_data2, 'decision_at_ns')
    
if __name__ == '__main__':
    run()
