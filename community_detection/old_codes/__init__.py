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
FREE, POB = 0, 5
MIN_LINKAGE_NUM, MIN_LINKAGE_RATIO = 2, 0.2


linkage_dir = taxi_data + '/linkage'
charts_dir = taxi_data + '/charts'
check_dir_create(taxi_data); check_dir_create(linkage_dir); check_dir_create(charts_dir)
#
grid_info_fn = taxi_data+ '/hl_vl_zones.pkl'
out_boundary_logs_fn = taxi_data+ '/out_boundary.txt'



ONE_HOUR, SIX_HOUR, EIGHT_HOUR = 1, 6, 8
HOUR12, HOUR24 = 12, 24
THRESHOLD_VALUE = 30 * 60

#


def get_processed_log_fn(time_from, time_to):
    return taxi_data + "/pl-%s-%s.csv" % (str(time_from[0]) + ''.join(['%02d' % d for d in time_from[1:]]),
                                       str(time_to[0]) + ''.join(['%02d' % d for d in time_to[1:]]))
