from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import information_boards.__init__
#
from taxi_common.file_handling_functions import check_dir_create
#
from information_boards.__init__ import taxi_data
check_dir_create(taxi_data)
trips_dir, trip_prefix = taxi_data + '/trips', 'trip-'
#
from information_boards.__init__ import summary_dir
check_dir_create(summary_dir)
ap_tm_num_dur_fare_fn = summary_dir + '/ap-tm-num-dur-fare.csv' 
ns_tm_num_dur_fare_fn = summary_dir + '/ns-tm-num-dur-fare.csv'
#