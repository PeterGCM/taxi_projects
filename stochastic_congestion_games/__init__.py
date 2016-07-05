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
#


# problem_result_dir = './problem_result'
# if os.path.exists(problem_result_dir): shutil.rmtree(problem_result_dir)
# os.makedirs(problem_result_dir)
# #
# problem_dir = problem_result_dir + '/problem'; os.makedirs(problem_dir)
# init_inputs_fn = problem_dir + '/init_inputs.txt'
# flow_fn, revenue_fn, cost_fn, dist_fn = \
#     problem_dir + '/flow.txt', problem_dir + '/revenue.txt', problem_dir + '/cost.txt', problem_dir + '/dist.txt'
# #
# policy_dir = problem_result_dir + '/policy'; os.makedirs(policy_dir)
# policy_prefix = policy_dir + '/policy-'
# #
# x_dir = problem_result_dir + '/x'; os.makedirs(x_dir)
# x_prefix = x_dir + '/x-'
# #
# dist_dir = problem_result_dir + '/dist'; os.makedirs(dist_dir)
# dist_prefix = dist_dir + '/dist-'
# #
# lp_dir = problem_result_dir + '/lp'; os.makedirs(lp_dir)
# lp_prefix = lp_dir+ '/LP-MODEL-'