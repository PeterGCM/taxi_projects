import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'
check_dir_create(taxi_data)
#
# Trip mode define
#
ap_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '/src/airport_polygon'
ns_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '/src/night_safari_polygon'
DIn_PIn, DIn_POut, DOut_PIn, DOut_POut = range(4)
IN, OUT = True, False
#
AM2, AM5 = 2, 5
NUM, DUR, FARE = range(3)
# For meaningless data filtering
error_hours = [('9', '3', '15', '1'), ('10', '3', '17', '1'), ('10', '7', '4', '6'), ('10', '7', '4', '7'), ('10', '7', '4', '8'),
               # second filtering
                ('10', '3', '17', '6'), ('10', '11', '21', '6'), ('10', '11', '21', '10'),  # Abnormal (long) queueing time
                ('9', '3', '1', '1'), ('9', '11', '8', '1'), ('10', '5', '16', '1'), ('10', '1', '24', '1')  # Abnormal (short) active duration
               ]
#
ALL_DUR, ALL_FARE, ALL_NUM, \
AP_DUR, AP_FARE, AP_QUEUE, AP_NUM, \
NS_DUR, NS_FARE, NS_QUEUE, NS_NUM = range(11)
#
# directory path and file's prefix
#
trip_dpath, trip_prefix = '%s/%s' % (taxi_data, 'trip'), 'trip-'
trip_ap_summary_fpath = '%s/trip-ap-summary.csv' % (trip_dpath)
trip_ns_summary_fpath = '%s/trip-ns-summary.csv' % (trip_dpath)
#
crossingTime_dpath = '%s/%s' % (taxi_data, 'crossingTime')
crossingTime_ap_dpath, crossingTime_ap_prefix = '%s/%s' % (crossingTime_dpath, 'ap'), 'crossingTime-ap-'
crossingTime_ns_dpath, crossingTime_ns_prefix = '%s/%s' % (crossingTime_dpath, 'ns'), 'crossingTime-ns-'
log_dpath, log_prefix = '%s/%s' % (crossingTime_dpath, 'log'), 'log-'
log_last_day_dpath, log_last_day_prefix ='%s/%s' % (crossingTime_dpath, 'log_last_day'), 'log-last-day-'
#
queueingTime_dpath = '%s/%s' % (trip_dpath, 'queueingTime')
queueingTime_ap_dpath, queueingTime_ap_prefix = '%s/%s' % (queueingTime_dpath, 'ap'), 'trip-queueingTime-ap-'
queueingTime_ns_dpath, queueingTime_ns_prefix = '%s/%s' % (queueingTime_dpath, 'ns'), 'trip-queueingTime-ns-'
#
productivity_dpath, productivity_prefix = '%s/%s' % (taxi_data , 'productivity'), 'productivity-'
productivity_summary_fpath = '%s/productivity-summary.csv' % productivity_dpath
shift_dpath, shift_prefix = '/home/sfcheng/toolbox/results', 'shift-hour-state-'
shiftProDur_dpath, shiftProDur_prefix = '%s/%s' % (productivity_dpath, 'shiftProDur'), 'shiftProDur-'
#
economicProfit_dpath = '%s/%s' % (trip_dpath, 'economicProfit')
economicProfit_ap_dpath, economicProfit_ap_prefix = '%s/%s' % (economicProfit_dpath, 'ap'), 'trip-EP-ap-'
economicProfit_ns_dpath, economicProfit_ns_prefix = '%s/%s' % (economicProfit_dpath, 'ns'), 'trip-EP-ns-'
#
ssDriver_dpath = '%s/%s' % (taxi_data, 'ssDriver')
ssDriverTrip_dpath, ssDriverTrip_prefix = '%s/%s' % (ssDriver_dpath, 'ssDriverTrip'), 'ssDriverTrip-'
ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix = '%s/%s' % (ssDriver_dpath, 'ssDriverShiftProDur'), 'ssDriverShiftProDur-'
ssDriverEP_dpath = '%s/%s' % (ssDriver_dpath, 'ssDriverEP')
ssDriverEP_ap_dpath, ssDriverEP_ap_prefix = '%s/%s' % (ssDriverEP_dpath, 'ap'), 'ssDriverEP-ap-'
ssDriverEP_ns_dpath, ssDriverEP_ns_prefix = '%s/%s' % (ssDriverEP_dpath, 'ns'), 'ssDriverEP-ns-'
# Units
SEC3600, SEC60 = 60 * 60, 60
CENT = 100
Q_LIMIT_MIN = 0
DAY_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TIME_SLOTS = range(24)



