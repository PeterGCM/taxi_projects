import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'
check_dir_create(taxi_data)
#
linkage_dir = taxi_data + '/linkage'
charts_dir = taxi_data + '/charts'
check_dir_create(taxi_data); check_dir_create(linkage_dir); check_dir_create(charts_dir)
#
grid_info_fn = taxi_data+ '/hl_vl_zones.pkl'
out_boundary_logs_fn = taxi_data+ '/out_boundary.txt'

FREE, POB = 0, 5



MAX_LINKAGE_RATIO = 0.8
MIN_LINKAGE = 2
SIX_HOUR = 6
EIGHT_HOUR = 8
ONE_HOUR = 1
HOUR24 = 24
HOUR12 = 12
THRESHOLD_VALUE = 30 * 60
COINCIDENCE_THRESHOLD_VALUE = 1

MEMORY_MANAGE_INTERVAL = 24 * 60 * 60
#


def get_processed_log_fn(time_from, time_to):
    return taxi_data + "/pl-%s-%s.csv" % (str(time_from[0]) + ''.join(['%02d' % d for d in time_from[1:]]),
                                       str(time_to[0]) + ''.join(['%02d' % d for d in time_to[1:]]))
