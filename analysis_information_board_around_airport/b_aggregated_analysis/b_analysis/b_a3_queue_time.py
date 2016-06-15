from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import Y09_ap_trips, Y10_ap_trips, Y09_ns_trips, Y10_ns_trips
from supports._setting import SEC60
from supports._setting import DInAP_PInAP, DOutAP_PInAP
from supports._setting import DInNS_PInNS, DOutNS_PInNS
from supports._setting import TIME_SLOTS
from supports.charts import histo_cumulative, x_twin_chart
#
import pandas as pd
import scipy.stats as stats
#
def run():
    #
    ap_analysis()
    ns_analysis()

def ap_analysis():
    Y09, Y10 = pd.read_csv(Y09_ap_trips), pd.read_csv(Y10_ap_trips)
    draw_cumulative_histogram('ap', Y09, Y10, 'ap')
    assert False
    #
    Y09_prev_in, Y09_prev_out = Y09[Y09['ap-trip-mode'] == DInAP_PInAP], Y09[Y09['ap-trip-mode'] == DOutAP_PInAP]
    Y10_prev_in, Y10_prev_out = Y10[Y10['ap-trip-mode'] == DInAP_PInAP], Y10[Y10['ap-trip-mode'] == DOutAP_PInAP]
    #
    Y09_in_hourly_gb, Y10_in_hourly_gb = Y09_prev_in.groupby(['hh']), Y10_prev_in.groupby(['hh'])
    Y09_out_hourly_gb, Y10_out_hourly_gb = Y09_prev_out.groupby(['hh']), Y10_prev_out.groupby(['hh'])
    Y09_in_hourly_qt = [ x / SEC60 for x in Y09_in_hourly_gb.mean()['ap-queue-time']]
    Y10_in_hourly_qt = [ x / SEC60 for x in Y10_in_hourly_gb.mean()['ap-queue-time']]
    in_diff = [Y09_in_hourly_qt[i] - Y10_in_hourly_qt[i] for i in xrange(len(Y09_in_hourly_qt))]
    Y09_in_hourly_num = [ x for x in Y09_in_hourly_gb.count()['ap-queue-time']]
    Y10_in_hourly_num = [ x for x in Y10_in_hourly_gb.count()['ap-queue-time']]
    in_num = [Y10_in_hourly_num[i] + Y09_in_hourly_num[i] for i in xrange(len(Y09_in_hourly_num))]
    Y09_out_hourly_qt = [ x / SEC60 for x in Y09_out_hourly_gb.mean()['ap-queue-time']]
    Y10_out_hourly_qt = [ x / SEC60 for x in Y10_out_hourly_gb.mean()['ap-queue-time']]
    out_diff = [Y09_out_hourly_qt[i] - Y10_out_hourly_qt[i] for i in xrange(len(Y09_out_hourly_qt))]
    Y09_out_hourly_num = [ x for x in Y09_out_hourly_gb.count()['ap-queue-time']]
    Y10_out_hourly_num = [ x for x in Y10_out_hourly_gb.count()['ap-queue-time']]
    out_num = [Y10_out_hourly_num[i] + Y09_out_hourly_num[i] for i in xrange(len(Y09_out_hourly_num))]
    #
    x_info = ('Time slot', TIME_SLOTS, 0)
    y_info1 = ('Minute', [Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff], (-5, 125), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [in_num], (0, 350000), ['Number of airport trips'], 'upper right') 
    x_twin_chart((12, 6), '', x_info, y_info1, y_info2, 'time_slot_queue_time_in_ap')
    print '----------------------T-test in_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_in_hourly_qt, Y10_in_hourly_qt))
    #
    x_info = ('Time slot', TIME_SLOTS, 0)
    y_info1 = ('Minute', [Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff], (-5, 125), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [out_num], (0, 350000), ['Number of airport trips'], 'upper right') 
    x_twin_chart((12, 6), '', x_info, y_info1, y_info2, 'time_slot_queue_time_out_ap')
    print '----------------------T-test out_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_out_hourly_qt, Y10_out_hourly_qt))

def ns_analysis():
    Y09, Y10 = pd.read_csv(Y09_ns_trips), pd.read_csv(Y10_ns_trips)
#     draw_cumulative_histogram('ns', Y09, Y10)
    #
    Y09_prev_in, Y09_prev_out = Y09[Y09['ns-trip-mode'] == DInNS_PInNS], Y09[Y09['ns-trip-mode'] == DOutNS_PInNS]
    Y10_prev_in, Y10_prev_out = Y10[Y10['ns-trip-mode'] == DInNS_PInNS], Y10[Y10['ns-trip-mode'] == DOutNS_PInNS]
    #
    Y09_in_hourly_gb, Y10_in_hourly_gb = Y09_prev_in.groupby(['hh']), Y10_prev_in.groupby(['hh'])
    Y09_out_hourly_gb, Y10_out_hourly_gb = Y09_prev_out.groupby(['hh']), Y10_prev_out.groupby(['hh'])
    Y09_in_hourly_qt = [ x / SEC60 for x in Y09_in_hourly_gb.mean()['ns-queue-time']]
    Y10_in_hourly_qt = [ x / SEC60 for x in Y10_in_hourly_gb.mean()['ns-queue-time']]
    in_diff = [Y09_in_hourly_qt[i] - Y10_in_hourly_qt[i] for i in xrange(len(Y09_in_hourly_qt))]
    Y09_in_hourly_num = [ x for x in Y09_in_hourly_gb.count()['ns-queue-time']]
    Y10_in_hourly_num = [ x for x in Y10_in_hourly_gb.count()['ns-queue-time']]
    in_num = [Y10_in_hourly_num[i] + Y09_in_hourly_num[i] for i in xrange(len(Y09_in_hourly_num))]
    Y09_out_hourly_qt = [ x / SEC60 for x in Y09_out_hourly_gb.mean()['ns-queue-time']]
    Y10_out_hourly_qt = [ x / SEC60 for x in Y10_out_hourly_gb.mean()['ns-queue-time']]
    out_diff = [Y09_out_hourly_qt[i] - Y10_out_hourly_qt[i] for i in xrange(len(Y09_out_hourly_qt))]
    Y09_out_hourly_num = [ x for x in Y09_out_hourly_gb.count()['ns-queue-time']]
    Y10_out_hourly_num = [ x for x in Y10_out_hourly_gb.count()['ns-queue-time']]
    out_num = [Y10_out_hourly_num[i] + Y09_out_hourly_num[i] for i in xrange(len(Y09_out_hourly_num))]
    #
    x_info = ('Time slot', [19,20,21,22,23], 0)
    y_info1 = ('Minute', [Y09_in_hourly_qt, Y10_in_hourly_qt, in_diff], (-5, 40), ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [in_num], (0, 30000), ['Number of night safari trips'], 'upper right') 
    x_twin_chart((6, 6), '', x_info, y_info1, y_info2, 'time_slot_queue_time_in_ns')
    print '----------------------T-test in_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_in_hourly_qt, Y10_in_hourly_qt))
    x_info = ('Time slot', [19,20,21,22,23], 0)
    y_info1 = ('Minute', [Y09_out_hourly_qt, Y10_out_hourly_qt, out_diff], None, ['Y2009', 'Y2010', 'Diff.'], 'upper left')
    y_info2 = ('', [out_num], (0, 30000), ['Number of night safari trips'], 'upper right') 
    x_twin_chart((6, 6), '', x_info, y_info1, y_info2, 'time_slot_queue_time_out_ns')
    print '----------------------T-test out_hourly_qt'
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_rel(Y09_out_hourly_qt, Y10_out_hourly_qt))

def draw_cumulative_histogram(location, Y09, Y10, fn_postfix):
    temp_Y09, temp_Y10 = [ x / SEC60 for x in Y09['%s-queue-time' % location]], [ x / SEC60 for x in Y10['%s-queue-time' % location]]
    filtering_boundary = 120
    x1, x2 = [x for x in temp_Y09 if x < filtering_boundary], [x for x in temp_Y10 if x < filtering_boundary]
    print '----------------------the number of filtered data (%s)' % location
    print 'Y09: %d(%.2f%%), Y09: %d(%.2f%%)' % (len(temp_Y09) - len(x1),
                                            (len(temp_Y09) - len(x1)) / len(temp_Y09) * 100,
                                            len(temp_Y10) - len(x2),
                                            (len(temp_Y10) - len(x2)) / len(temp_Y10) * 100)
    #
    print '----------------------T-test (%s)' % location
    print 't statistics %.3f, p-value %.3f' % (stats.ttest_ind(x1, x2, equal_var=False))
    num_bin = 30
    histo_cumulative('', 'Minute', '', num_bin, [x1, x2], ['Y2009', 'Y2010'], save_fn='cum_histo_qt_%s' % fn_postfix)

if __name__ == '__main__':
    run()
