from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path, get_taxi_data_path
from taxi_common.file_handling_functions import check_dir_create
taxi_home, taxi_data = get_taxi_home_path(), get_taxi_data_path()
#
scg_dir = taxi_data + '/stochastic_congestion_games'
check_dir_create(scg_dir)
#
problem_dir = scg_dir + '/problems'
check_dir_create(problem_dir)
