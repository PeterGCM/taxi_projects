from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path, get_taxi_data_path
from taxi_common.file_handling_functions import check_dir_create
taxi_home, taxi_data = get_taxi_home_path(), get_taxi_data_path()
#
cd_home = taxi_data + '/community_data'
linkage_dir = cd_home + '/linkage'
check_dir_create(cd_home); check_dir_create(linkage_dir)
#
grid_info_fn = cd_home + '/hl_vl_zones.pkl'
out_boundary_logs_fn = cd_home + '/out_boundary.txt'





THRESHOLD_VALUE = 30 * 60
COINCIDENCE_THRESHOLD_VALUE = 1
FREE, POB = 0, 5
MEMORY_MANAGE_INTERVAL = 24 * 60 * 60
#


def get_processed_log_fn(time_from, time_to):
    return cd_home + "/pl-%s-%s.csv" % (str(time_from[0]) + ''.join(['%02d' % d for d in time_from[1:]]),
                                       str(time_to[0]) + ''.join(['%02d' % d for d in time_from[1:]]))
