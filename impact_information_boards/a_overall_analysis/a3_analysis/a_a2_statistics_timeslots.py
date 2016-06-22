from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn
#
from supports._setting import DAY_OF_WEEK, TIME_SLOTS, CENT
from supports._setting import DInAP_PInAP, DOutAP_PInAP
from supports._setting import DInNS_PInNS, DOutNS_PInNS
from supports.charts import multiple_line_chart
#
import pandas as pd

def run():
#     general_analysis()
    ap_analysis()
#     ns_analysis()
    
def general_analysis():
    whole = pd.read_csv(ap_tm_num_dur_fare_fn)
    wh_gb = whole.groupby(['hh', 'day-of-week'])
    #
    # Total Number of whole trips
    # 
    UNIT = 1000
    hour_dow_totalNumTrip = wh_gb.sum()['num-tm'].to_frame('total-num-trip').reset_index()
    xs = range(len(TIME_SLOTS))
    yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
    for hour, dow, totalNumTrip in hour_dow_totalNumTrip.values:
        yss[DAY_OF_WEEK.index(dow)][hour] += totalNumTrip / UNIT
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'Unit 1,000',
                        (xs, 0), yss, DAY_OF_WEEK, 'upper left', 'wh_num_trips')
    #
    # Total fare of whole trips
    #
    UNIT = 1000000
    hour_dow_totalFare = wh_gb.sum()['total-fare'].to_frame('total-fare').reset_index()
    xs = range(len(TIME_SLOTS))
    yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
    for hour, dow, totalFare in hour_dow_totalFare.values:
        yss[DAY_OF_WEEK.index(dow)][hour] += (totalFare / CENT) / UNIT
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'Unit S$ 1,000,000',
                        (xs, 0), yss, DAY_OF_WEEK, 'upper left', 'wh_fare_trips')

def ap_analysis():
    whole = pd.read_csv(ap_tm_num_dur_fare_fn)
    in_ap = whole[(whole['ap-trip-mode'] == DInAP_PInAP) | (whole['ap-trip-mode'] == DOutAP_PInAP)]
    in_ap_gb = in_ap.groupby(['hh', 'day-of-week'])
    #
    # Total number of airport trips
    # 
    UNIT = 1000
    hour_dow_totalNumTrip = in_ap_gb.sum()['num-tm'].to_frame('total-num-trip').reset_index()
    xs = range(len(TIME_SLOTS))
    yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
    for hour, dow, totalNumTrip in hour_dow_totalNumTrip.values:
        yss[DAY_OF_WEEK.index(dow)][hour] += totalNumTrip / UNIT
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'Unit 1,000',
                        (xs, 0), yss, DAY_OF_WEEK, 'upper left', 'in_ap_num_trips')
    #
    # Total fare of in airport trips
    #
    UNIT = 1000000
    hour_dow_totalFare = in_ap_gb.sum()['total-fare'].to_frame('total-fare').reset_index()
    xs = range(len(TIME_SLOTS))
    yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
    for hour, dow, totalFare in hour_dow_totalFare.values:
        yss[DAY_OF_WEEK.index(dow)][hour] += (totalFare / CENT) / UNIT
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'S$ 1,000,000', 
                        (xs, 0), yss, DAY_OF_WEEK, 'upper left', 'in_ap_fare')


def ns_analysis():
    whole = pd.read_csv(ns_tm_num_dur_fare_fn)
    ns = whole[(whole['ns-trip-mode'] == DInNS_PInNS) | (whole['ns-trip-mode'] == DOutNS_PInNS)]
    ns_gb = ns.groupby(['hh', 'day-of-week'])
    #
    # Total number of night safari trips
    # 
    UNIT = 1000
    hour_dow_totalNumTrip = ns_gb.sum()['num-tm'].to_frame('total-num-trip').reset_index()
    xs = range(len(TIME_SLOTS))
    yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
    for hour, dow, totalNumTrip in hour_dow_totalNumTrip.values:
        yss[DAY_OF_WEEK.index(dow)][hour] += totalNumTrip / UNIT
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'Number of trips (Unit 1,000)', (xs, 0), yss, DAY_OF_WEEK, 'upper left', 'in_ns_num_trips')                    
    #
    # Total fare of night safari trips
    #
    UNIT = 1000
    hour_dow_totalFare = ns_gb.sum()['total-fare'].to_frame('total-fare').reset_index()
    xs = range(len(TIME_SLOTS))
    yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
    for hour, dow, totalFare in hour_dow_totalFare.values:
        yss[DAY_OF_WEEK.index(dow)][hour] += (totalFare / CENT) / UNIT
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'Fare (Unit S$ 1,000)', (xs, 0), yss, DAY_OF_WEEK, 'upper left', 'in_ns_fare_trips')
    
if __name__ == '__main__':
    run()
