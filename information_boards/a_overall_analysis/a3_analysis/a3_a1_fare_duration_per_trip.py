import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from __init__ import CENT, SEC60
from a_overall_analysis.__init__ import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn  # @UnresolvedImport
#
from taxi_common.charts import simple_barchart  # @UnresolvedImport
#
import pandas as pd
#
def run():
    for fn, l, x0_lable in [(ap_tm_num_dur_fare_fn, 'ap', 'Airport'),
                            (ns_tm_num_dur_fare_fn, 'ns', 'Night safari')]:
        trip_df = pd.read_csv(fn)
        gb = trip_df.groupby('trip-mode')
        #
        # calculate statistics
        #
        in_num = gb.sum()['num-tm'][DIn_PIn] + gb.sum()['num-tm'][DOut_PIn]
        in_fare = (gb.sum()['total-fare'][DIn_PIn] + gb.sum()['total-fare'][DOut_PIn]) / CENT
        in_dur = (gb.sum()['total-dur'][DIn_PIn] + gb.sum()['total-dur'][DOut_PIn]) / SEC60
        #
        in_fare_per_trip = in_fare / in_num
        in_dur_per_trip = in_dur / in_num
        #
        out_num = gb.sum()['num-tm'][DIn_POut] + gb.sum()['num-tm'][DOut_POut]
        out_fare = (gb.sum()['total-fare'][DIn_POut] + gb.sum()['total-fare'][DOut_POut]) / CENT
        out_dur = (gb.sum()['total-dur'][DIn_POut] + gb.sum()['total-dur'][DOut_POut]) / SEC60
        #
        out_fare_per_trip = out_fare / out_num
        out_dur_per_trip = out_dur / out_num
        #
        # charts
        #
        _data = [in_fare_per_trip, out_fare_per_trip]
        simple_barchart([x0_lable, 'Other areas'], 'S$', _data, 'fare_per_trip_%s' % l)
        #
        _data = [in_dur_per_trip, out_dur_per_trip]
        simple_barchart([x0_lable, 'Other areas'], 'Minute', _data, 'dur_per_trip_%s' % l)

if __name__ == '__main__':
    run()
