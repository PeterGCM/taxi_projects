from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.file_handling_functions import check_dir_create  # @UnresolvedImport
#
from init_project import taxi_data
check_dir_create(taxi_data)
# 
trips_dir, trip_prefix = taxi_data + '/trips', 'trip-'
ap_trips_dir, ap_trip_prefix = trips_dir + '/ap_trips', 'ap-trip-'
ns_trips_dir, ns_trip_prefix = trips_dir + '/ns_trips', 'ns-trip-'
#
from init_project import summary_dir
check_dir_create(summary_dir)
ap_tm_num_dur_fare_fn = summary_dir + '/ap-tm-num-dur-fare.csv' 
ns_tm_num_dur_fare_fn = summary_dir + '/ns-tm-num-dur-fare.csv'
#
