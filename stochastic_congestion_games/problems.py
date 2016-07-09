import stochastic_congestion_games.__init__
#
from stochastic_congestion_games.__init__ import problem_dir
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, save_pickle_file, load_pickle_file
#
from random import randrange, seed
from prettytable import PrettyTable
import numpy as np

problem_saving_dir = None


def p0():
    # Manually generated problem
    # This is only for Reinforcement learning because this problem has single time slot
    global problem_saving_dir
    problem_saving_dir = problem_dir + '/Problem0'
    if not check_path_exist(problem_saving_dir):
        check_dir_create(problem_saving_dir)
        num_agents, num_zones, time_horizon = 10, 2, 1
        fl = [[
                [2, 2],
                [7, 8]
                ]]; assert len(fl) == time_horizon; assert len(fl[0]) == num_zones
        Re = [[
                [2, 10],
                [8, 3]
                ]]; assert len(Re) == time_horizon; assert len(Re[0]) == num_zones
        Co = [[
                [1, 4],
                [3, 2]
                ]]; assert len(Co) == time_horizon; assert len(Co[0]) == num_zones
        Ds =  [[
                [1, 2],
                [3, 1]
                ]]; assert len(Ds) == time_horizon; assert len(Ds[0]) == num_zones
        d0 = [8, 2]; assert sum(d0) == num_agents
        save_pickle_file(problem_saving_dir + '/p0.pkl', [num_agents, num_zones, time_horizon, fl, Re, Co, Ds, d0])
    else:
        num_agents, num_zones, time_horizon, fl, Re, Co, Ds, d0 = load_pickle_file(problem_saving_dir + '/p0.pkl')
    return num_agents, num_zones, time_horizon, fl, Re, Co, Ds, d0, problem_saving_dir



def p1():
    global problem_saving_dir
    problem_saving_dir = problem_dir + '/Problem1'
    if not check_path_exist(problem_saving_dir):
        check_dir_create(problem_saving_dir)
        #
        num_agents, num_zones, time_horizon = 10, 3, 3; save_init_inputs(num_agents, num_zones, time_horizon)
        #
        # seed(1)
        flow_lb, flow_ub = 1, int(num_agents * 1.5)
        reward_lb, reward_ub = 1, 100
        fl = flow_generation(flow_lb, flow_ub, num_zones, time_horizon)
        Re, Co = reward_cost_generation(reward_lb, reward_ub, time_horizon, num_zones)
        d0 = distribution_generation(num_agents, num_zones)
        save_pickle_file(problem_saving_dir + '/p1.pkl', [num_agents, num_zones, time_horizon, fl, Re, Co, d0])
    else:
        num_agents, num_zones, time_horizon, fl, Re, Co, d0 = load_pickle_file(problem_saving_dir + '/p1.pkl')
    return num_agents, num_zones, time_horizon, fl, Re, Co, d0, problem_saving_dir


def p2():
    global problem_saving_dir
    problem_saving_dir = problem_dir + '/Problem 2'
    if not check_path_exist(problem_saving_dir):
        check_dir_create(problem_saving_dir)
        #
        num_agents, num_zones, time_horizon = 14, 5, 5; save_init_inputs(num_agents, num_zones, time_horizon)
        #
        # seed(10)
        flow_lb, flow_ub = 1, int(num_agents / num_zones)
        reward_lb, reward_ub = 20, 100
        fl = flow_generation(flow_lb, flow_ub, num_zones, time_horizon)
        Re, Co = reward_cost_generation(reward_lb, reward_ub, time_horizon, num_zones)
        d0 = distribution_generation(num_agents, num_zones)
        save_pickle_file(problem_saving_dir + '/p1.pkl', [num_agents, num_zones, time_horizon, fl, Re, Co, d0])
    else:
        num_agents, num_zones, time_horizon, fl, Re, Co, d0 = load_pickle_file(problem_saving_dir + '/p1.pkl')
    return num_agents, num_zones, time_horizon, fl, Re, Co, d0, problem_saving_dir

def save_init_inputs(num_agents, num_zones, H):
    with open(problem_saving_dir + '/init_inputs.txt', 'w') as f:
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
    with open(problem_saving_dir + '/flow.txt', 'w') as f:
        f.write('Flow description -----------------------------------\n')
        problem_saving_table_representation(f, fl)
    return fl


def reward_cost_generation(reward_lb, reward_ub, time_horizon, num_zones):
    Re = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    Co = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    for t in xrange(time_horizon):
        for i in xrange(num_zones):
            costs = [randrange(int(reward_ub * 0.5)) for _ in xrange(num_zones)]
            min_cost_id = np.argmin(costs)
            min_cost = costs[min_cost_id]
            i_cost = costs[i]
            costs[i] = min_cost
            costs[min_cost_id] = i_cost
            rewards = [randrange(costs[x] + 1, reward_ub) for x in xrange(num_zones)]
            Re[t][i], Co[t][i] = rewards[:], costs[:]

    # Re = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    # Co = [[[0] * num_zones for _ in xrange(num_zones)] for _ in xrange(time_horizon)]
    # for t in xrange(time_horizon):
    #     for i in xrange(num_zones):
    #         for j in xrange(num_zones):
    #             reward = randrange(reward_lb, reward_ub)
    #             while reward == reward_lb:
    #                 reward = randrange(reward_lb, reward_ub)
    #             cost = randrange(reward)
    #             Re[t][i][j], Co[t][i][j] = reward, cost

    with open(problem_saving_dir + '/revenue.txt', 'w') as f:
        f.write('Revenue description -----------------------------------\n')
        problem_saving_table_representation(f, Re)
    with open(problem_saving_dir + '/cost.txt', 'w') as f:
        f.write('Cost description -----------------------------------\n')
        problem_saving_table_representation(f, Co)
        f.write('----------------------------------- \n')
    return Re, Co


def distribution_generation(num_agents, num_zones):
    d0 = [0] * num_zones
    for _ in xrange(num_agents):
        d0[randrange(num_zones)] += 1
    _table = PrettyTable([z for z in xrange(num_zones)])
    _table.add_row([d0[z] for z in xrange(num_zones)])
    with open(problem_saving_dir + '/dist.txt', 'w') as f:
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