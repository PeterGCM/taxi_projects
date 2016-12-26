from __future__ import division

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
from taxi_common.file_handling_functions import check_dir_create
#
from information_boards.__init__ import taxi_data, summary_dir
from information_boards.old_codes.a_overall_analysis import trips_dpath
check_dir_create(taxi_data)
check_dir_create(summary_dir)
#
# Log
#
logs_dir, log_prefix = '%s/%s' % (taxi_data, 'logs'), 'log-'
logs_last_day_dir, log_last_day_prefix = '%s/%s' % (logs_dir, 'logs_last_day'), 'log-last-day-'
ap_crossing_dir, ap_crossing_prefix = '%s/%s' % (logs_dir, 'ap_crossing'), 'ap-crossing-time-'
ns_crossing_dir, ns_crossing_prefix = '%s/%s' % (logs_dir, 'ns_crossing'), 'ns-crossing-time-'
#
# Trip
#
ap_trips_dir, ap_trip_prefix = '%s/%s' % (trips_dpath, 'ap_trips'), 'ap-trip-'
ns_trips_dir, ns_trip_prefix = '%s/%s' % (trips_dpath, 'ns_trips'), 'ns-trip-'

#
# Economic_profit
#
ep_dir = '%s/%s' % (taxi_data, 'trips_wEP')
ap_ep_dir, ap_ep_prefix = '%s/%s' % (ep_dir, 'ap_ep'), 'ap-ep-'
ns_ep_dir, ns_ep_prefix = '%s/%s' % (ep_dir, 'ns_ep'), 'ns-ep-'
#
# Shift
#
shifts_dir, shift_prefix = '/home/sfcheng/toolbox/results', 'shift-hour-state-'
shift_pro_dur_dir, shift_pro_dur_prefix = '%s/%s' % (taxi_data, 'shift_pro_dur'), 'shift-pro-dur-'
#
# Productivity
#
productivity_dir, productivity_prefix = '%s/%s' % (taxi_data , 'productivity'), 'productivity-'
#
#
#
hourly_stats_fpath = '%s/%s' % (summary_dir, 'hourly_stats.csv')


Y09_ap_trips = summary_dir + '/Y09-ap-trips.csv'
Y10_ap_trips = summary_dir + '/Y10-ap-trips.csv'
Y09_ns_trips = summary_dir + '/Y09-ns-trips.csv'
Y10_ns_trips = summary_dir + '/Y10-ns-trips.csv'
driver_monthly_fare_fn = summary_dir + '/driver-monthly-fare.pkl'