import __init__
#
from information_boards.__init__ import DIn_PIn, DOut_PIn
from information_boards.__init__ import charts_dir
from information_boards.__init__ import SEC60, TIME_SLOTS
from b_aggregated_analysis.__init__ import Y09_ap_trips, Y10_ap_trips, Y09_ns_trips, Y10_ns_trips
#
from taxi_common.file_handling_functions import check_dir_create
from taxi_common.charts import histo_cumulative, multiple_line_chart, x_twin_chart  # @UnresolvedImport
#
import pandas as pd
import scipy.stats as stats


def run():
    global a3_dir
    a3_dir = charts_dir + '/b_aggregated_a3 queueing time'
    check_dir_create(a3_dir)
    #
    # Airport
    #
    Y09, Y10 = pd.read_csv(Y09_ap_trips), pd.read_csv(Y10_ap_trips)
    draw_cumulative_histogram(Y09, Y10, 'ap')
    monthly_queueing_time_in_only(Y09, Y10, 'ap', TIME_SLOTS)
    monthly_queueing_time_num_trips(Y09, Y10, 'ap', TIME_SLOTS)
    #
    # Night safari
    #
    Y09, Y10 = pd.read_csv(Y09_ns_trips), pd.read_csv(Y10_ns_trips)
    Y09, Y10 = Y09[(Y09['hh'] > 18)], Y10[(Y10['hh'] > 18)]
    draw_cumulative_histogram(Y09, Y10, 'ns')
    monthly_queueing_time_in_only(Y09, Y10, 'ns', range(19, 24))
    monthly_queueing_time_num_trips(Y09, Y10, 'ns', range(19, 24))


def draw_cumulative_histogram(Y09, Y10, fn_postfix):
    temp_Y09, temp_Y10 = [x / float(SEC60) for x in Y09['queueing-time']], [x / float(SEC60) for x in Y10['queueing-time']]
    filtering_boundary = 120
    x1, x2 = [x for x in temp_Y09 if x < filtering_boundary], [x for x in temp_Y10 if x < filtering_boundary]
    print '----------------------the number of filtered data_20160826 (%s)' % fn_postfix
    print 'Y09: %d(%.2f%%), Y10: %d(%.2f%%)' % (len(temp_Y09) - len(x1),
                                            (len(temp_Y09) - len(x1)) / float(len(temp_Y09)) * 100,
                                            len(temp_Y10) - len(x2),
                                            (len(temp_Y10) - len(x2)) / float(len(temp_Y10)) * 100)
    #
    print '----------------------T-test (%s)' % fn_postfix
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_ind(x1, x2, equal_var=False))
    num_bin = 30
    histo_cumulative('', 'Minute', '', num_bin, [x1, x2], ['Y2009', 'Y2010'], a3_dir + '/cum_histo_qt_%s' % fn_postfix)


def monthly_queueing_time_in_only(Y09, Y10, label, times):
    (Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff, _), _ = monthly_data_process(Y09, Y10)
    xs = times
    yss = [Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff]
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'Minute', (xs, 0), yss, 
                        ['Y2009', 'Y2010', 'Diff.'], 'upper right', a3_dir + '/qt_in_%s' % label)
    print '----------------------T-test in_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_in_hourly_qt, Y10_in_hourly_qt))


def monthly_queueing_time_num_trips(Y09, Y10, label, times):
    (Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff, in_num), \
    (Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff, out_num) = monthly_data_process(Y09, Y10) 
    #
    x_info = ('Time slot', times, 0)
    y_info1 = ('Minute', [Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff], (-5, 125), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [in_num], (0, 350000), ['Number of trips'], 'upper right') 
    x_twin_chart((12, 6), '', x_info, y_info1, y_info2, a3_dir + '/qt_num_in_%s' % label)
    print '----------------------T-test in_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_in_hourly_qt, Y10_in_hourly_qt))
    #
    x_info = ('Time slot', times, 0)
    y_info1 = ('Minute', [Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff], (-5, 125), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [out_num], (0, 350000), ['Number of trips'], 'upper right') 
    x_twin_chart((12, 6), '', x_info, y_info1, y_info2, a3_dir + '/qt_num_out_%s' % label)
    print '----------------------T-test out_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_out_hourly_qt, Y10_out_hourly_qt))
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_out_hourly_qt, Y10_out_hourly_qt))


def monthly_data_process(Y09, Y10):
    Y09_prev_in, Y09_prev_out = Y09[Y09['trip-mode'] == DIn_PIn], Y09[Y09['trip-mode'] == DOut_PIn]
    Y10_prev_in, Y10_prev_out = Y10[Y10['trip-mode'] == DIn_PIn], Y10[Y10['trip-mode'] == DOut_PIn]
    #
    Y09_in_hourly_gb, Y10_in_hourly_gb = Y09_prev_in.groupby(['hh']), Y10_prev_in.groupby(['hh'])
    Y09_out_hourly_gb, Y10_out_hourly_gb = Y09_prev_out.groupby(['hh']), Y10_prev_out.groupby(['hh'])
    Y09_in_hourly_qt = [ x / float(SEC60) for x in Y09_in_hourly_gb.mean()['queueing-time']]
    Y10_in_hourly_qt = [ x / float(SEC60) for x in Y10_in_hourly_gb.mean()['queueing-time']]
    in_diff = [Y09_in_hourly_qt[i] - Y10_in_hourly_qt[i] for i in xrange(len(Y09_in_hourly_qt))]
    Y09_in_hourly_num = [ x for x in Y09_in_hourly_gb.count()['queueing-time']]
    Y10_in_hourly_num = [ x for x in Y10_in_hourly_gb.count()['queueing-time']]
    in_num = [Y10_in_hourly_num[i] + Y09_in_hourly_num[i] for i in xrange(len(Y09_in_hourly_num))]
    Y09_out_hourly_qt = [ x / float(SEC60) for x in Y09_out_hourly_gb.mean()['queueing-time']]
    Y10_out_hourly_qt = [ x / float(SEC60) for x in Y10_out_hourly_gb.mean()['queueing-time']]
    out_diff = [Y09_out_hourly_qt[i] - Y10_out_hourly_qt[i] for i in xrange(len(Y09_out_hourly_qt))]
    Y09_out_hourly_num = [ x for x in Y09_out_hourly_gb.count()['queueing-time']]
    Y10_out_hourly_num = [ x for x in Y10_out_hourly_gb.count()['queueing-time']]
    out_num = [Y10_out_hourly_num[i] + Y09_out_hourly_num[i] for i in xrange(len(Y09_out_hourly_num))]
    #
    return (Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff, in_num), (Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff, out_num) 

if __name__ == '__main__':
    run()
