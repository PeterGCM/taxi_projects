from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import driver_monthly_fare_gt, driver_monthly_fare_at, driver_monthly_fare_nt
from supports._setting import charts_dir, row_data_b_a1
from supports.etc_functions import check_dir_create, write_text_file, load_picle_file
from supports.charts import one_histogram
#
from scipy import stats
import numpy as np
#
def run():
    check_dir_create(charts_dir)
    write_text_file(row_data_b_a1, 'Init', True)
    #
    general_analysis()
    ap_analysis()
    ns_analysis()
    
def general_analysis():
    write_text_file(row_data_b_a1, 'General analysis----------------------------------')
    Y09, Y10 = load_picle_file(driver_monthly_fare_gt)
    write_text_file(row_data_b_a1, '----------------------T-test')
    write_text_file(row_data_b_a1,
            't statistics %.3f, p-value %.3f' % (stats.ttest_ind(Y09, Y10, equal_var=False)))
    #
    num_bin = 50
    #
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y09, save_fn='Y2009_driver_monthly_fares')
    #
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y10, save_fn='Y2010_driver_monthly_fares')
    
def ap_analysis():
    write_text_file(row_data_b_a1, 'Airport analysis----------------------------------')
    Y09, Y10 = load_picle_file(driver_monthly_fare_at)
    #
    write_text_file(row_data_b_a1, '----------------------T-test')
    write_text_file(row_data_b_a1,
            't statistics %.3f, p-value %.3f' % (stats.ttest_ind(Y09, Y10, equal_var=False)))
    #
    num_bin = 15
    #
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y09, save_fn='Y2009_driver_monthly_fares_ap')
    #
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y10, save_fn='Y2010_driver_monthly_fares_ap')
    #
    num_bin = 12
    #
    one_histogram('', 'Fare log10(S$)', 'Probability', num_bin, np.log10(Y09), save_fn='Y2009_driver_monthly_fares_ap_log')
    #
    one_histogram('', 'Fare log10(S$)', 'Probability', num_bin, np.log10(Y10), save_fn='Y2010_driver_monthly_fares_ap_log')
    
def ns_analysis():
    write_text_file(row_data_b_a1, 'Night safari analysis----------------------------------')
    Y09, Y10 = load_picle_file(driver_monthly_fare_nt)
    #
    write_text_file(row_data_b_a1, '----------------------T-test')
    write_text_file(row_data_b_a1,
            't statistics %.3f, p-value %.3f' % (stats.ttest_ind(Y09, Y10, equal_var=False)))
    #
    num_bin = 15
    #
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y09, save_fn='Y2009_driver_monthly_fares_ns')
    #
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y10, save_fn='Y2010_driver_monthly_fares_ns')
    num_bin = 12
    #
    one_histogram('', 'Fare log10(S$)', 'Probability', num_bin, np.log10(Y09), save_fn='Y2009_driver_monthly_fares_ns_log')
    #
    one_histogram('', 'Fare log10(S$)', 'Probability', num_bin, np.log10(Y10), save_fn='Y2010_driver_monthly_fares_ns_log')

if __name__ == '__main__':
    run()
