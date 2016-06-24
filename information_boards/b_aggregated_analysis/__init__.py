from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
import init_project
#
from taxi_common.file_handling_functions import check_dir_create
#
from init_project import taxi_data
check_dir_create(taxi_data)
logs_dir, log_prefix = taxi_data + '/logs', 'log-'
log_last_day_dir = logs_dir + '/logs_last_day'