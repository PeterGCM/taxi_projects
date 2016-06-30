import __init__  # @UnresolvedImport # @UnusedImport
#
from b_aggregated_analysis.__init__ import driver_monthly_fare_fn
#
from taxi_common.file_handling_functions import load_pickle_file
#
from taxi_common.charts import one_histogram
#
from scipy import stats
#
def run():
    #
    general_analysis()

def general_analysis():
    Y09, Y10 = load_pickle_file(driver_monthly_fare_fn)
    num_bin = 50
    #
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_ind(Y09, Y10, equal_var=False))
    #
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y09, save_fn='Y2009_monthly_fares')
    one_histogram('', 'Fare (S$)', 'Probability', num_bin, Y10, save_fn='Y2010_monthly_fares')

if __name__ == '__main__':
    run()
