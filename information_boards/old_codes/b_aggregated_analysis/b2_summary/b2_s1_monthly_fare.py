import __init__
#
from information_boards.__init__ import CENT
from a_overall_analysis.__init__ import trips_dir, trip_prefix
from b_aggregated_analysis.__init__ import driver_monthly_fare_fn
#
from taxi_common.file_handling_functions import save_pickle_file
#
import pandas as pd
#
def run():
    Y09_monthly_fare, Y10_monthly_fare = [], []
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
            trip_df = trip_df[(trip_df['did'] != -1)]
            #
            fares = [x / float(CENT) for x in list(trip_df.groupby(['did']).sum()['fare'])]
            if y == 9:
                Y09_monthly_fare += fares
            else:
                Y10_monthly_fare += fares
    save_pickle_file(driver_monthly_fare_fn, [Y09_monthly_fare, Y10_monthly_fare])
            
if __name__ == '__main__':
    run()