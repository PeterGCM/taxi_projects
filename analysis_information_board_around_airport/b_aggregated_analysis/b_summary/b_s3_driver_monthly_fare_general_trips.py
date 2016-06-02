from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import trips_dir, trip_prefix
from supports._setting import summary_dir, driver_monthly_fare_gt
from supports.etc_functions import check_dir_create
from supports._setting import CENT
from supports.etc_functions import save_pickle_file
#
import pandas as pd
#
def run():
    check_dir_create(summary_dir)
    #
    Y09_driver_total_monthly_fare, Y10_driver_total_monthly_fare= [], []
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            trip_df = pd.read_csv('%s/%s%s.csv' % (trips_dir, trip_prefix, yymm))
            trip_df = trip_df[(trip_df['did'] != -1)]
            #
            fares = [ x / CENT for x in list(trip_df.groupby(['did']).sum()['fare'])]
            if y == 9:
                Y09_driver_total_monthly_fare += fares
            else:
                Y10_driver_total_monthly_fare += fares
    save_pickle_file(driver_monthly_fare_gt, [Y09_driver_total_monthly_fare, Y10_driver_total_monthly_fare])
            
if __name__ == '__main__':
    run()