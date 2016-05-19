from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/..')
#
from supports.etc_functions import check_dir_create
from supports._setting import Y09_ap_trips, Y10_ap_trips
from supports._setting import summary_dir, driver_monthly_fare_at
from supports._setting import CENT
from supports.handling_pkl import save_pickle_file
#
import pandas as pd
#
def run():
    check_dir_create(summary_dir)
    #
    Y09, Y10 = pd.read_csv(Y09_ap_trips), pd.read_csv(Y10_ap_trips)
    Y09 = Y09[(Y09['did'] != -1)]; Y10 = Y10[(Y10['did'] != -1)]
    #
    Y09_mm_did_gb, Y10_mm_did_gb = Y09.groupby(['mm', 'did']), Y10.groupby(['mm', 'did'])
    Y09_ap_fares = [ x / CENT for x in list(Y09_mm_did_gb.sum()['fare'])]
    Y10_ap_fares = [ x / CENT for x in list(Y10_mm_did_gb.sum()['fare'])]
    #
    save_pickle_file(driver_monthly_fare_at, [Y09_ap_fares, Y10_ap_fares])
            
if __name__ == '__main__':
    run()
