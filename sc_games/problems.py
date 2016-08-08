import stochastic_congestion_games.__init__
#
from __init__ import SEED_NUM
from stochastic_congestion_games.__init__ import problem_dir
from taxi_common.file_handling_functions import check_dir_create, check_path_exist, save_pickle_file, load_pickle_file
#
from random import randrange, seed
# from prettytable import PrettyTable
import numpy as np


def sc_game0():
    seed(SEED_NUM)
    #
    num_agents, S, A = 5, range(2), range(2)
    Tr_sas = [
        [[.5, .5],  # s0 = 0
         [.5, .5]],
        [[.5, .5],  # s0 = 1
         [.5, .5]]
    ]
    # Only dependent on the number of state
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (-2, 0),
                        (-3, 0)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] * ds + reward_constants[ai][1]
    ags_S = [0, 1, 1, 0, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game1():
    seed(SEED_NUM)
    #
    num_agents, S, A = 5, range(2), range(2)
    Tr_sas = [
        [[.2, .8],  # s0 = 0
         [.3, .7]],
        [[.5, .5],  # s0 = 1
         [.7, .3]]
    ]
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (-2, 2),
                        (-3, 5)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] * ds + reward_constants[ai][1]
    ags_S = [0, 1, 1, 0, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game2():
    seed(SEED_NUM)
    #
    num_agents, S, A = 10, range(2), range(2)
    Tr_sas = [
        [[.2, .8],  # s0 = 0
         [.3, .7]],
        [[.5, .5],  # s0 = 1
         [.7, .3]]
    ]
    # Only dependent on the number of state
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (-2, 0),
                        (-8, 0)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] * ds + reward_constants[ai][1]
    ags_S = [0, 1, 1, 0, 1, 0, 1, 1, 0, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def sc_game3():
    seed(SEED_NUM)
    #
    num_agents, S, A = 10, range(2), range(2)
    Tr_sas = [
        [[.2, .8],  # s0 = 0
         [.3, .7]],
        [[.5, .5],  # s0 = 1
         [.7, .3]]
    ]
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (-2, 4),
                        (-8, 10)]; assert len(reward_constants) == len(A)
    R = lambda si, ai, ds: reward_constants[ai][0] * ds + reward_constants[ai][1]
    ags_S = [0, 1, 1, 0, 1, 0, 1, 1, 0, 1]; assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


if __name__ == '__main__':
    pass
