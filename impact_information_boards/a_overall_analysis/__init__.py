from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from init_project import taxi_data
#
trips_dir, trip_prefix = taxi_data + '/trips', 'trip-'
ap_trips_dir, ap_trip_prefix = trips_dir + '/ap_trips', 'ap-trip-'
ns_trips_dir, ns_trip_prefix = trips_dir + '/ns_trips', 'ns-trip-'
#
