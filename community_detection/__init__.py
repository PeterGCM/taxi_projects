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
grid_info_fn = taxi_data+ '/hl_vl_zones.pkl'
#
logs_dir = taxi_data + '/logs'; out_boundary_logs_fn = logs_dir+ '/out_boundary.txt'
linkage_dir = taxi_data + '/linkage'
edge_dir = taxi_data + '/edge'
for _dir in [logs_dir, linkage_dir, edge_dir]:
    check_dir_create(_dir)
#
FREE, POB = 0, 5
THRESHOLD_VALUE = 30 * 60
MIN_LINKAGE_NUM, MIN_LINKAGE_RATIO = 2, 0.2
ONE_HOUR, SIX_HOUR, EIGHT_HOUR, HOUR12, HOUR24 = 1, 6, 8, 12, 24
#



charts_dir = taxi_data + '/charts'
#
