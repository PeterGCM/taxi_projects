import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import DIn_PIn, DIn_POut, DOut_PIn, DOut_POut
from __init__ import SEC60, TIME_SLOTS
from b_aggregated_analysis.__init__ import Y09_ap_trips, Y10_ap_trips, Y09_ns_trips, Y10_ns_trips
#
from taxi_common.charts import histo_cumulative, multiple_line_chart, x_twin_chart  # @UnresolvedImport
#
import pandas as pd
import scipy.stats as stats
#
def run():
    #
    for label, Y09_fn, Y10_fn in [('ap', Y09_ap_trips, Y10_ap_trips),
                                  ('ns', Y09_ns_trips, Y10_ns_trips)]:
        Y09, Y10 = pd.read_csv(Y09_fn), pd.read_csv(Y10_fn)
        draw_cumulative_histogram(Y09, Y10, label)
        monthly_queueing_time_in_only(Y09, Y10, label)
        monthly_queueing_time_num_trips(Y09, Y10, label)
    
def draw_cumulative_histogram(Y09, Y10, fn_postfix):
    temp_Y09, temp_Y10 = [x / SEC60 for x in Y09['queueing-time']], [x / SEC60 for x in Y10['queueing-time']]
    filtering_boundary = 120
    x1, x2 = [x for x in temp_Y09 if x < filtering_boundary], [x for x in temp_Y10 if x < filtering_boundary]
    print '----------------------the number of filtered data (%s)' % fn_postfix
    print 'Y09: %d(%.2f%%), Y09: %d(%.2f%%)' % (len(temp_Y09) - len(x1),
                                            (len(temp_Y09) - len(x1)) / len(temp_Y09) * 100,
                                            len(temp_Y10) - len(x2),
                                            (len(temp_Y10) - len(x2)) / len(temp_Y10) * 100)
    #
    print '----------------------T-test (%s)' % fn_postfix
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_ind(x1, x2, equal_var=False))
    num_bin = 30
    histo_cumulative('', 'Minute', '', num_bin, [x1, x2], ['Y2009', 'Y2010'], save_fn='cum_histo_qt_%s' % fn_postfix)

def monthly_queueing_time_in_only(Y09, Y10, label):
    (Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff, _), _ = monthly_data_process(Y09, Y10)
    xs = range(len(TIME_SLOTS))
    yss = [Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff]
    #
    multiple_line_chart((12, 6), '', 'Time slot', 'Minute', (xs, 0), yss, 
                        ['Y2009', 'Y2010', 'Diff.'], 'upper right', 'in_trips_qt_%s' % label)
    print '----------------------T-test in_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_in_hourly_qt, Y10_in_hourly_qt))

def monthly_queueing_time_num_trips(Y09, Y10, label):
    (Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff, in_num), \
    (Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff, out_num) = monthly_data_process(Y09, Y10) 
    #
    x_info = ('Time slot', TIME_SLOTS, 0)
    y_info1 = ('Minute', [Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff], (-5, 125), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [in_num], (0, 350000), ['Number of trips'], 'upper right') 
    x_twin_chart((12, 6), '', x_info, y_info1, y_info2, 'in_qt_num_%s' % label)
    print '----------------------T-test in_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_in_hourly_qt, Y10_in_hourly_qt))
    #
    x_info = ('Time slot', TIME_SLOTS, 0)
    y_info1 = ('Minute', [Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff], (-5, 125), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [out_num], (0, 350000), ['Number of trips'], 'upper right') 
    x_twin_chart((12, 6), '', x_info, y_info1, y_info2, 'out_qt_num_%s' % label)
    print '----------------------T-test out_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_out_hourly_qt, Y10_out_hourly_qt))
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_out_hourly_qt, Y10_out_hourly_qt))

def monthly_data_process(Y09, Y10):
    Y09_prev_in, Y09_prev_out = Y09[Y09['trip-mode'] == DIn_PIn], Y09[Y09['trip-mode'] == DOut_PIn]
    Y10_prev_in, Y10_prev_out = Y10[Y10['trip-mode'] == DIn_PIn], Y10[Y10['trip-mode'] == DOut_PIn]
    #
    Y09_in_hourly_gb, Y10_in_hourly_gb = Y09_prev_in.groupby(['hh']), Y10_prev_in.groupby(['hh'])
    Y09_out_hourly_gb, Y10_out_hourly_gb = Y09_prev_out.groupby(['hh']), Y10_prev_out.groupby(['hh'])
    Y09_in_hourly_qt = [ x / SEC60 for x in Y09_in_hourly_gb.mean()['queueing-time']]
    Y10_in_hourly_qt = [ x / SEC60 for x in Y10_in_hourly_gb.mean()['queueing-time']]
    in_diff = [Y09_in_hourly_qt[i] - Y10_in_hourly_qt[i] for i in xrange(len(Y09_in_hourly_qt))]
    Y09_in_hourly_num = [ x for x in Y09_in_hourly_gb.count()['queueing-time']]
    Y10_in_hourly_num = [ x for x in Y10_in_hourly_gb.count()['queueing-time']]
    in_num = [Y10_in_hourly_num[i] + Y09_in_hourly_num[i] for i in xrange(len(Y09_in_hourly_num))]
    Y09_out_hourly_qt = [ x / SEC60 for x in Y09_out_hourly_gb.mean()['queueing-time']]
    Y10_out_hourly_qt = [ x / SEC60 for x in Y10_out_hourly_gb.mean()['queueing-time']]
    out_diff = [Y09_out_hourly_qt[i] - Y10_out_hourly_qt[i] for i in xrange(len(Y09_out_hourly_qt))]
    Y09_out_hourly_num = [ x for x in Y09_out_hourly_gb.count()['queueing-time']]
    Y10_out_hourly_num = [ x for x in Y10_out_hourly_gb.count()['queueing-time']]
    out_num = [Y10_out_hourly_num[i] + Y09_out_hourly_num[i] for i in xrange(len(Y09_out_hourly_num))]
    
    return (Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff, in_num), (Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff, out_num) 

if __name__ == '__main__':
    run()
