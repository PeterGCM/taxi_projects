import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data_20160826'
check_dir_create(taxi_data)
#
logs_dir = taxi_data + '/logs'
trips_dir = taxi_data + '/trips'
for _dir in [logs_dir, trips_dir]:
    check_dir_create(_dir)

FREE = 0
HOUR1, HOUR12 = 1, 12




grid_info_fn = 'hl_vl_zones.pkl'
#
get_processed_log_fn = lambda time_from, time_to: 'processed-log-%s-%s.csv' % (get_str_timeformat(time_from), get_str_timeformat(time_to))
get_processed_trip_fn = lambda time_from, time_to: 'processed-trip-%s-%s.csv' % (get_str_timeformat(time_from), get_str_timeformat(time_to))
def get_str_timeformat(time_tuple):
    return str(time_tuple[0]) + ''.join(['%02d' % d for d in time_tuple[1:]])
#
TIMESLOT_LENGTH = 60 * 60
def get_timeslot(time_from_ts, t):
    return int((t - time_from_ts) / TIMESLOT_LENGTH)
         
    
