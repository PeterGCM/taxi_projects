import __init__
#
from information_boards.__init__ import charts_dir
from b_aggregated_analysis.__init__ import driver_monthly_fare_fn
#
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create
from taxi_common.charts import one_histogram
#
from scipy import stats


def run():
    a1_dir = charts_dir + '/b_aggregated_a1 monthly fare'
    check_dir_create(a1_dir)
    #
    Y09, Y10 = load_pickle_file(driver_monthly_fare_fn)
    num_bin = 50
    #
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_ind(Y09, Y10, equal_var=False))
    #
    one_histogram((8,6), '', 'Fare (S$)', 'Probability', num_bin, Y09, a1_dir + '/Y2009_monthly_fares')
    one_histogram((8,6), '', 'Fare (S$)', 'Probability', num_bin, Y10, a1_dir + '/Y2010_monthly_fares')

if __name__ == '__main__':
    run()
