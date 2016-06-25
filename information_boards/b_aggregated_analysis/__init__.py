from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import init_project
#
from taxi_common.file_handling_functions import check_dir_create
#
from init_project import taxi_data
check_dir_create(taxi_data)
logs_dir, log_prefix = taxi_data + '/logs', 'log-'
logs_last_day_dir, log_last_day_prefix = logs_dir + '/logs_last_day', 'log-last-day-'
ap_crossing_dir, ap_crossing_prefix = logs_dir + '/ap_crossing', 'ap-crossing-time-'
ns_crossing_dir, ns_crossing_prefix = logs_dir + '/ns_crossing', 'ns-crossing-time-'
#
from a_overall_analysis.__init__ import trips_dir
ap_trips_dir, ap_trip_prefix = trips_dir + '/ap_trips', 'ap-trip-'
ns_trips_dir, ns_trip_prefix = trips_dir + '/ns_trips', 'ns-trip-'