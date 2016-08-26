import stochastic_congestion_games.__init__
#
from sc_games import SEED_NUM
from stochastic_congestion_games.__init__ import problem_dir
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, save_pickle_file, load_pickle_file
#
from random import randrange, seed
# from prettytable import PrettyTable
import numpy as np


def sc_game0():
    seed(SEED_NUM)
    #
    num_agents, S, A = 3, range(2), range(2)
    Tr_sas = [
        [[1.0, .0],  # s0 = 0
         [.0, 1.0]],
        [[1.0, .0],  # s0 = 1
         [.0, 1.0]]
    ]
    # Only dependent on the number of state
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (-1, 0),
                        (-2.5, 0)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] * ds + reward_constants[ai][1]
    ags_S = [0, 1, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game1():
    seed(SEED_NUM)
    #
    num_agents, S, A = 3, range(2), range(2)
    Tr_sas = [
        [[1.0, .0],  # s0 = 0
         [.0, 1.0]],
        [[1.0, .0],  # s0 = 1
         [.0, 1.0]]
    ]
    # Only dependent on the number of state
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (1, 0),
                        (2.5, 0)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
    ags_S = [0, 1, 1]; assert len(ags_S) == num_agents
    #
    #
    #
    from __init__ import ALPH, GAMMA, EPSILON
    # V = {}
    # Vds_max = {}
    # for ds in range(1, num_agents + 1):
    #     for a in A:
    #         V[ds, a] = 0
    #     Vds_max[ds] = 0
    # while True:
    #     v_max = -1e400
    #     for ds in range(1, num_agents + 1):
    #         _v = R(None, ds, 0) + R(None, num_agents - ds, 1)











    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game2():
    seed(SEED_NUM)
    #
    num_agents, S, A = 10, range(2), range(2)
    Tr_sas = [
        [[1.0, .0],  # s0 = 0
         [.0, 1.0]],
        [[1.0, .0],  # s0 = 1
         [.0, 1.0]]
    ]
    # Only dependent on the number of state
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (8, 0),
                        (12, 0)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game3():
    seed(SEED_NUM)
    #
    num_agents, S, A = 10, range(2), range(2)
    Tr_sas = [
        [[.8, .2],  # s0 = 0
         [.1, .9]],
        [[.7, .3],  # s0 = 1
         [.2, .8]]
    ]
    # Only dependent on the number of state
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (8, 2),
                        (12, 5)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game4():
    seed(SEED_NUM)
    #
    num_agents, S, A = 10, range(2), range(2)
    Tr_sas = [
        [[.8, .2],  # s0 = 0
         [.1, .9]],
        [[.7, .3],  # s0 = 1
         [.2, .8]]
    ]
    # Only dependent on the number of state
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (8, 2),
                        (12, 5)]; assert len(reward_constants) == len(A)
    # R = lambda si, ai, ds: reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
    def R(si, ai, ds):
        actual_reward = reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
        variance = actual_reward * 0.1
        return np.random.uniform(actual_reward - variance, actual_reward + variance)
    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game5():
    seed(SEED_NUM)
    # Big problem


if __name__ == '__main__':
    sc_game1()
