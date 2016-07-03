from __future__ import division
#
import os, shutil
#

problem_dir = './problems'



problem_result_dir = './problem_result'
if os.path.exists(problem_result_dir): shutil.rmtree(problem_result_dir)
os.makedirs(problem_result_dir)
#
problem_dir = problem_result_dir + '/problem'; os.makedirs(problem_dir)
init_inputs_fn = problem_dir + '/init_inputs.txt'
flow_fn, revenue_fn, cost_fn, dist_fn = \
    problem_dir + '/flow.txt', problem_dir + '/revenue.txt', problem_dir + '/cost.txt', problem_dir + '/dist.txt'
#
policy_dir = problem_result_dir + '/policy'; os.makedirs(policy_dir)
policy_prefix = policy_dir + '/policy-'
#
x_dir = problem_result_dir + '/x'; os.makedirs(x_dir)
x_prefix = x_dir + '/x-'
#
dist_dir = problem_result_dir + '/dist'; os.makedirs(dist_dir)
dist_prefix = dist_dir + '/dist-'
#
lp_dir = problem_result_dir + '/lp'; os.makedirs(lp_dir)
lp_prefix = lp_dir+ '/LP-MODEL-'