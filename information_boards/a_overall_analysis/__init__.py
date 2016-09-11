import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
from information_boards import taxi_data, summary_dir
from taxi_common.file_handling_functions import check_dir_create
#
trips_dpath, trip_prefix = '%s/%s' % (taxi_data, 'trips'), 'trip-'
#
overall_summary_dptah = '%s/%s' % (summary_dir, 'overall_analysis')
check_dir_create(overall_summary_dptah)
ap_tm_num_dur_fare_fpath = '%s/%s' % (overall_summary_dptah, 'ap-tm-num-dur-fare.csv')
ns_tm_num_dur_fare_fpath = '%s/%s' % (overall_summary_dptah, 'ns-tm-num-dur-fare.csv')
#
NUM, DUR, FARE = range(3)