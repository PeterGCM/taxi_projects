from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import information_boards.__init__
#
from taxi_common.file_handling_functions import check_dir_create
#
from information_boards.__init__ import taxi_data, summary_dir
from a_overall_analysis.__init__ import trips_dir
check_dir_create(taxi_data)
check_dir_create(summary_dir)
#
# Log
#
logs_dir, log_prefix = taxi_data + '/logs', 'log-'
logs_last_day_dir, log_last_day_prefix = logs_dir + '/logs_last_day', 'log-last-day-'
ap_crossing_dir, ap_crossing_prefix = logs_dir + '/ap_crossing', 'ap-crossing-time-'
ns_crossing_dir, ns_crossing_prefix = logs_dir + '/ns_crossing', 'ns-crossing-time-'
#
# Trip
#
ap_trips_dir, ap_trip_prefix = trips_dir + '/ap_trips', 'ap-trip-'
ns_trips_dir, ns_trip_prefix = trips_dir + '/ns_trips', 'ns-trip-'
Y09_ap_trips = summary_dir + '/Y09-ap-trips.csv'
Y10_ap_trips = summary_dir + '/Y10-ap-trips.csv'
Y09_ns_trips = summary_dir + '/Y09-ns-trips.csv'
Y10_ns_trips = summary_dir + '/Y10-ns-trips.csv'
#
# Economic_profit
#
ep_dir = taxi_data + '/economic_profit'
ap_ep_dir, ap_ep_prefix = ep_dir + '/ap_ep', 'ap-ep-'
ns_ep_dir, ns_ep_prefix = ep_dir + '/ns_ep', 'ns-ep-'
#
# Shift
#
shifts_dir, shift_prefix = '/home/sfcheng/toolbox/results', 'shift-hour-state-'
shift_pro_dur_dir, shift_pro_dur_prefix = taxi_data + '/shift_pro_dur', 'shift-pro-dur-'
#
# Productivity
#
productivity_dir, productivity_prefix = taxi_data + '/productivity', 'productivity-'
hourly_stats_fpath = summary_dir + '/hourly_stats.csv'
zero_duration_timeslots = summary_dir + '/zero-duration-time-slots.pkl'
#
#
#
driver_monthly_fare_fn = summary_dir + '/driver-monthly-fare.pkl'