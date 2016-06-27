import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import DIn_PIn, DOut_PIn
from __init__ import CENT
from __init__ import DAY_OF_WEEK, TIME_SLOTS
from a_overall_analysis.__init__ import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn  # @UnresolvedImport
#
from taxi_common.charts import multiple_line_chart  # @UnresolvedImport
#
import pandas as pd

def run():
    whole_df = pd.read_csv(ap_tm_num_dur_fare_fn)
    ap_df = whole_df[(whole_df['trip-mode'] == DIn_PIn) | (whole_df['trip-mode'] == DOut_PIn)]
    whole_df = pd.read_csv(ns_tm_num_dur_fare_fn)
    ns_df = whole_df[(whole_df['trip-mode'] == DIn_PIn) | (whole_df['trip-mode'] == DOut_PIn)]
    for df, num_unit, num_chart_fn, fare_unit, fare_chart_fn in [(whole_df, 1000, 'timeslot_wh_num', 1000000, 'timeslot_wh_fare'),
                                                                 (ap_df, 1000, 'timeslot_ap_num', 1000000, 'timeslot_ap_fare'),
                                                                 (ns_df, 1000, 'timeslot_ns_num', 1000, 'timeslot_ns_fare')]:
        df_gb = df.groupby(['hh', 'day-of-week'])
        #
        # Total Number of trips
        # 
        hour_dow_totalNumTrip = df_gb.sum()['num-tm'].to_frame('total-num-trip').reset_index()
        xs = range(len(TIME_SLOTS))
        yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
        for hour, dow, totalNumTrip in hour_dow_totalNumTrip.values:
            yss[DAY_OF_WEEK.index(dow)][hour] += totalNumTrip / num_unit
        #
        
        multiple_line_chart((12, 6), '', 'Time slot', 'Unit %s' % format(num_unit, ",d"),
                            (xs, 0), yss, DAY_OF_WEEK, 'upper left', num_chart_fn)
        #
        # Total fare of trips
        #
        hour_dow_totalFare = df_gb.sum()['total-fare'].to_frame('total-fare').reset_index()
        xs = range(len(TIME_SLOTS))
        yss = [[0] * len(TIME_SLOTS) for _ in DAY_OF_WEEK]
        for hour, dow, totalFare in hour_dow_totalFare.values:
            yss[DAY_OF_WEEK.index(dow)][hour] += (totalFare / CENT) / fare_unit
        #
        multiple_line_chart((12, 6), '', 'Time slot', 'Unit S$ %s' % format(fare_unit, ",d"),
                            (xs, 0), yss, DAY_OF_WEEK, 'upper left', fare_chart_fn)
    
if __name__ == '__main__':
    run()
