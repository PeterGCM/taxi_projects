import __init__
#
from information_boards.__init__ import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from information_boards.__init__ import CENT, SEC60
from information_boards.__init__ import charts_dir
from a_overall_analysis.__init__ import ap_tm_num_dur_fare_fn, ns_tm_num_dur_fare_fn
#
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.charts import simple_barchart  # @UnresolvedImport
#
import pandas as pd


def run():
    a1_dir = charts_dir + '/a_a1 fare and duration per trip'
    check_dir_create(a1_dir)
    for fn, l, x0_label in [(ap_tm_num_dur_fare_fn, 'ap', 'Airport'),
                            (ns_tm_num_dur_fare_fn, 'ns', 'Night safari')]:
        trip_df = pd.read_csv(fn)
        gb = trip_df.groupby('trip-mode')
        #
        # calculate statistics
        #
        in_num = gb.sum()['total-num'][DIn_PIn] + gb.sum()['total-num'][DOut_PIn]
        in_fare = (gb.sum()['total-fare'][DIn_PIn] + gb.sum()['total-fare'][DOut_PIn]) / float(CENT)
        in_dur = (gb.sum()['total-dur'][DIn_PIn] + gb.sum()['total-dur'][DOut_PIn]) / float(SEC60)
        #
        in_fare_per_trip = in_fare / float(in_num)
        in_dur_per_trip = in_dur / float(in_num)
        #
        out_num = gb.sum()['total-num'][DIn_POut] + gb.sum()['total-num'][DOut_POut]
        out_fare = (gb.sum()['total-fare'][DIn_POut] + gb.sum()['total-fare'][DOut_POut]) / float(CENT)
        out_dur = (gb.sum()['total-dur'][DIn_POut] + gb.sum()['total-dur'][DOut_POut]) / float(SEC60)
        #
        out_fare_per_trip = out_fare / float(out_num)
        out_dur_per_trip = out_dur / float(out_num)
        #
        # charts
        #
        _data = [in_fare_per_trip, out_fare_per_trip]
        simple_barchart([x0_label, 'Other areas'], 'S$', _data, a1_dir + '/fare_per_trip_%s' % l)
        #
        _data = [in_dur_per_trip, out_dur_per_trip]
        simple_barchart([x0_label, 'Other areas'], 'Minute', _data, a1_dir + '/dur_per_trip_%s' % l)

if __name__ == '__main__':
    run()
