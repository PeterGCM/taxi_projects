import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
from information_boards import taxi_data, summary_dir
#
trips_dpath, trip_prefix = '%s/%s' % (taxi_data, 'trips'), 'trip-'
#
ap_tm_num_dur_fare_fpath = '%s/%s' % (summary_dir, 'ap-tm-num-dur-fare.csv')
ns_tm_num_dur_fare_fpath = '%s/%s' % (summary_dir, 'ns-tm-num-dur-fare.csv')
#
NUM, DUR, FARE = range(3)