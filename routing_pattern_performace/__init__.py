from __future__ import division
import os, sys
from math import ceil
#
sys.path.append(os.getcwd() + '/..')
#
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
         
    
