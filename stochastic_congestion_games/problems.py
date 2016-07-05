import __init__
#
from __init__ import problem_dir
from taxi_common.file_handling_functions import check_dir_create
#
from random import randrange, seed
from prettytable import PrettyTable


def p1():
    p1_dir = problem_dir + '/Problem 1'
    check_dir_create(p1_dir)
    #
    num_agents, num_zones, time_horizon = 10, 3, 3; save_init_inputs(num_agents, num_zones, H)
    #
    seed(1)
    flow_lb, flow_ub = 1, int(num_agents * 1.5)
    reward_lb, reward_ub = 1, 100
    fl = flow_generation(flow_lb, flow_ub, num_zones, time_horizon)
    Re, Co = reward_cost_generation(reward_lb, reward_ub, time_horizon, num_zones)
    d0 = distribution_generation(num_agents, num_zones)

    return num_agents, num_zones, time_horizon, fl, Re, Co, d0


def save_init_inputs(num_agents, num_zones, H):
    with open(init_inputs_fn, 'w') as f:
        f.write('Initial inputs ---------------------------------------------\n')
        f.write('Number of agents: %d, Number of zones: %d, Time horizon: %d\n' % (num_agents, num_zones, H))


def flow_generation(flow_lb, flow_ub, num_zones, time_horizon):
    #
    # fl: the first index represents time
    #        the second represents row
    #        the third represents column
    #
    fl = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    for t in xrange(time_horizon):
        for i in xrange(num_zones):
            for j in xrange(num_zones):
                fl[t][i][j] = randrange(flow_lb, flow_ub)
    with open(flow_fn, 'w') as f:
        f.write('Flow description -----------------------------------\n')
        problem_saving_table_representation(f, fl)
    return fl


def reward_cost_generation(reward_lb, reward_ub, time_horizon, num_zones):
    Re = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    Co = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    for t in xrange(time_horizon):
        for i in xrange(num_zones):
            for j in xrange(num_zones):
                reward = randrange(reward_lb, reward_ub)
                while reward == REWARD_LB:
                    reward = randrange(reward_lb, reward_ub)
                cost = randrange(reward)
                Re[t][i][j], Co[t][i][j] = reward, cost
    with open(revenue_fn, 'w') as f:
        f.write('Revenue description -----------------------------------\n')
        problem_saving_table_representation(f, Re)
    with open(cost_fn, 'w') as f:
        f.write('Cost description -----------------------------------\n')
        problem_saving_table_representation(f, Co)
        f.write('----------------------------------- \n')
    return Re, Co


def distribution_generation(num_agents, num_zones):
    d0 = [0] * num_zones
    for _ in xrange(num_agents):
        d0[randrange(num_zones)] += 1
    if RESULT_SAVE:
        _table = PrettyTable([z for z in xrange(num_zones)])
        _table.add_row([d0[z] for z in xrange(num_zones)])
        with open(dist_fn, 'w') as f:
            f.write('----------------------------------- Initial distribution\n')
            f.write('%s\n' % _table.get_string())
    return d0


def problem_saving_table_representation(f, _data):
    H, num_zones = len(_data), len(_data[0])
    f.write('Column represents FROM and Row represents TO\n')
    for t in xrange(H):
        f.write('t = %d,\n' % t)
        _table = PrettyTable([''] + [TO for TO in xrange(num_zones)])
        for FROM in xrange(num_zones):
            _table.add_row([FROM] + [_data[t][FROM][TO] for TO in xrange(num_zones)])
        f.write('%s\n' % _table.get_string())


if __name__ == '__main__':
    p1()

    # num_agents, num_zones = 10, 3
    # time_horizon = 5
    # generate_problem(num_agents, num_zones, time_horizon)