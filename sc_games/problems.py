import __init__
#
from sc_games import taxi_data
from sc_games import SEED_NUM, EPSILON
from sc_games import R_CONSTANT, R_LINEAR, R_INVERSE, R_EXPONENTIAL
from sc_games import T_SIMPLE, T_COMPLEX
from sc_games import SH_PARAMETER, SH_REWARD, SH_TRANSITION
from sc_games import PAR_L_ID_NUM_AGENT, PAR_L_ID_NUM_STATE, PAR_L_ID_R_TYPE, PAR_L_ID_Tr_TYPE, PAR_L_ID_AC, PAR_L_ID_DS
from sc_games import rtype_rname, ttype_tname, sheet_names, parameter_labels
#
from taxi_common.file_handling_functions import get_all_directories, check_dir_create
#
from random import seed, random, choice
import numpy as np
import xlwt


def problem_generator(num_agents, num_states, reward_type, transition_type):
    #
    # Record inputs for problem generation
    #
    num_agents, S, A = num_agents, range(num_states), range(num_states)
    problem_dn = 'P%d-G(%d)-S(%d)-R(%s)-Tr(%s)' % \
                  (len(get_all_directories(taxi_data)), num_agents, num_states,
                   rtype_rname[reward_type], ttype_tname[transition_type])
    problem_dpath = '%s/%s' % (taxi_data, problem_dn); check_dir_create(problem_dpath)
    problem_fpath = '%s/%s.xls' % (problem_dpath, problem_dn)
    workbook = xlwt.Workbook()
    par_sheet = workbook.add_sheet(sheet_names[SH_PARAMETER])
    for i, v in [(PAR_L_ID_NUM_AGENT, num_agents), (PAR_L_ID_NUM_STATE, num_states),
                 (PAR_L_ID_R_TYPE, rtype_rname[reward_type]), (PAR_L_ID_Tr_TYPE, ttype_tname[transition_type])]:
        par_sheet.write(i, 0, parameter_labels[i]); par_sheet.write(i, 1, v)
    ags_S = [choice(S) for _ in xrange(num_agents)]
    par_sheet.write(PAR_L_ID_DS, 0, parameter_labels[PAR_L_ID_DS])
    par_sheet.write(PAR_L_ID_DS, 1, '(%s)' % ','.join([str(v) for v in ags_S]))
    #
    # Reward function (only consider non-increasing functions, because of congestion game's characteristic)
    #
    R = {}
    if reward_type == R_CONSTANT:
        # Don't care about ds
        ac = [choice(range(num_agents)) for _ in range(num_states)] # Constants depending on actions
        # All constant should be greater than or equal zero
        for v in ac:
            assert v >= 0
        for ds in range(num_agents + 1):
            for a in A:
                R[ds, a] = ac[a]
    elif reward_type == R_LINEAR:
        # Depending on ds
        ac = [-choice(range(1, num_agents)) for _ in range(num_states)]  # Constants depending on actions
        # All constant should be less than zero
        for v in ac:
            assert v < 0
        for ds in range(num_agents + 1):
            for a in A:
                R[ds, a] = ac[a] * ds
    elif reward_type == R_INVERSE:
        # Depending on ds
        ac = [choice(range(1, num_agents)) for _ in range(num_states)]  # Constants depending on actions
        # All constant should be greater than zero
        for v in ac:
            assert v > 0
        for ds in range(num_agents + 1):
            for a in A:
                if ds == 0:
                    R[ds, a] = 0
                else:
                    R[ds, a] = ac[a] / float(ds)
    else:
        reward_type == R_EXPONENTIAL
        # Depending on ds
        ac = [random() for _ in range(num_states)]  # Constants depending on actions
        # All constant should be between zero and one
        for v in ac:
            assert v > 0
            assert v < 1
        for ds in range(num_agents + 1):
            for a in A:
                if ds == 0:
                    R[ds, a] = 0
                else:
                    R[ds, a] = ac[a] ** float(ds)
    par_sheet.write(PAR_L_ID_AC, 0, parameter_labels[PAR_L_ID_AC])
    par_sheet.write(PAR_L_ID_AC, 1, '(%s)' % ','.join([str(v) for v in ac]))
    reward_sheet = workbook.add_sheet(sheet_names[SH_REWARD])
    for i, l in enumerate(['ds', 'a', 'R']):
        reward_sheet.write(0, i, l)
    next_row_num = 1
    for ds in range(num_agents + 1):
        for a in A:
            reward_sheet.write(next_row_num, 0, ds)
            reward_sheet.write(next_row_num, 1, a)
            reward_sheet.write(next_row_num, 2, R[ds, a])
            next_row_num += 1
    #
    # Transition probability
    #
    Tr = {}
    transition_sheet = workbook.add_sheet(sheet_names[SH_TRANSITION])
    if transition_type == T_SIMPLE:
        for i, l in enumerate(['s0', 'a', 's1', 'Tr']):
            transition_sheet.write(0, i, l)
        next_row_num = 1
        for s0 in S:
            for a in A:
                rv = [random() for _ in S]
                sum_rv = sum(rv)
                for s1 in S:
                    Tr[s0, a, s1] = rv[s1] / float(sum_rv)
                    transition_sheet.write(next_row_num, 0, s0)
                    transition_sheet.write(next_row_num, 1, a)
                    transition_sheet.write(next_row_num, 2, s1)
                    transition_sheet.write(next_row_num, 3, Tr[s0, a, s1])
                    next_row_num += 1
    else:
        assert transition_type == T_COMPLEX
        for i, l in enumerate(['s0', 'ds0', 'a', 's1', 'Tr']):
            transition_sheet.write(0, i, l)
        next_row_num = 1
        for s0 in S:
            for ds0 in range(num_agents + 1):
                for a in A:
                    rv = [random() for _ in S]
                    sum_rv = sum(rv)
                    for s1 in S:
                        Tr[s0, ds0, a, s1] = rv[s1] / float(sum_rv)
                        transition_sheet.write(next_row_num, 0, s0)
                        transition_sheet.write(next_row_num, 1, ds0)
                        transition_sheet.write(next_row_num, 2, a)
                        transition_sheet.write(next_row_num, 3, s1)
                        transition_sheet.write(next_row_num, 4, Tr[s0, ds0, a, s1])
                        next_row_num += 1
    #


    workbook.save(problem_fpath)


def scG_twoState():
    seed(SEED_NUM)
    #
    num_agents, S, A = 10, range(2), range(2)
    Tr_sas = {
        # s0, a0        # s0, a1
        (0, 0, 0): 0.7, (0, 1, 0): 0.3,
        (0, 0, 1): 0.3, (0, 1, 1): 0.7,

        # s1, a0        # s1, a1
        (1, 0, 0): 0.7, (1, 1, 0): 0.3,
        (1, 0, 1): 0.3, (1, 1, 1): 0.7,
    }
    # Validate the transition function
    validate_transition(Tr_sas, S, A)
    # Only dependent on the number of state
    reward_constants = [  # Reward depends on action and the number of agent same state
        # The first constant is relate to the number of state, another is just constant
        (8, 2),
        (12, 5)];
    assert len(reward_constants) == len(A)

    def R(ds, ai):
        if ds == 0:
            return 0
        actual_reward = reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
        return actual_reward

    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1];
    assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def scG_threeState():
    seed(SEED_NUM)
    #
    num_agents, S, A = 10, range(3), range(3)
    Tr_sas = {
        # s0, a0        # s0, a1        # s0, a2
        (0, 0, 0): 0.7, (0, 1, 0): 0.2, (0, 2, 0): 0.2,
        (0, 0, 1): 0.2, (0, 1, 1): 0.7, (0, 2, 1): 0.1,
        (0, 0, 2): 0.1, (0, 1, 2): 0.1, (0, 2, 2): 0.7,

        # s1, a0        # s1, a1        # s1, a2
        (1, 0, 0): 0.7, (1, 1, 0): 0.2, (1, 2, 0): 0.2,
        (1, 0, 1): 0.2, (1, 1, 1): 0.7, (1, 2, 1): 0.1,
        (1, 0, 2): 0.1, (1, 1, 2): 0.1, (1, 2, 2): 0.7,

        # s2, a0        # s2, a1        # s2, a2
        (2, 0, 0): 0.7, (2, 1, 0): 0.2, (2, 2, 0): 0.2,
        (2, 0, 1): 0.2, (2, 1, 1): 0.7, (2, 2, 1): 0.1,
        (2, 0, 2): 0.1, (2, 1, 2): 0.1, (2, 2, 2): 0.7,
    }
    # Validate the transition function
    validate_transition(Tr_sas, S, A)
    #
    reward_constants = [  # Reward depends on action and the number of agent same state
        # The first constant is relate to the number of state, another is just constant
        (4, 1),
        (5, 2),
        (7, 2),
    ];
    assert len(reward_constants) == len(A)

    def R(ds, ai):
        if ds == 0:
            return 0
        actual_reward = reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
        return actual_reward

    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1];
    assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def scG_fiveState():
    seed(SEED_NUM)
    #
    num_agents, S, A = 15, range(5), range(5)
    Tr_sas = {
        # s0, a0        # s0, a1        # s0, a2        # s0, a3        # s0, a4
        (0, 0, 0): 0.6, (0, 1, 0): 0.1, (0, 2, 0): 0.1, (0, 3, 0): 0.1, (0, 4, 0): 0.1,
        (0, 0, 1): 0.1, (0, 1, 1): 0.6, (0, 2, 1): 0.1, (0, 3, 1): 0.1, (0, 4, 1): 0.1,
        (0, 0, 2): 0.1, (0, 1, 2): 0.1, (0, 2, 2): 0.6, (0, 3, 2): 0.1, (0, 4, 2): 0.1,
        (0, 0, 3): 0.1, (0, 1, 3): 0.1, (0, 2, 3): 0.1, (0, 3, 3): 0.6, (0, 4, 3): 0.1,
        (0, 0, 4): 0.1, (0, 1, 4): 0.1, (0, 2, 4): 0.1, (0, 3, 4): 0.1, (0, 4, 4): 0.6,

        # s1, a0        # s1, a1        # s1, a2        # s1, a3        # s1, a4
        (1, 0, 0): 0.6, (1, 1, 0): 0.1, (1, 2, 0): 0.1, (1, 3, 0): 0.1, (1, 4, 0): 0.1,
        (1, 0, 1): 0.1, (1, 1, 1): 0.6, (1, 2, 1): 0.1, (1, 3, 1): 0.1, (1, 4, 1): 0.1,
        (1, 0, 2): 0.1, (1, 1, 2): 0.1, (1, 2, 2): 0.6, (1, 3, 2): 0.1, (1, 4, 2): 0.1,
        (1, 0, 3): 0.1, (1, 1, 3): 0.1, (1, 2, 3): 0.1, (1, 3, 3): 0.6, (1, 4, 3): 0.1,
        (1, 0, 4): 0.1, (1, 1, 4): 0.1, (1, 2, 4): 0.1, (1, 3, 4): 0.1, (1, 4, 4): 0.6,

        # s2, a0        # s2, a1        # s2, a2        # s2, a3        # s2, a4
        (2, 0, 0): 0.6, (2, 1, 0): 0.1, (2, 2, 0): 0.1, (2, 3, 0): 0.1, (2, 4, 0): 0.1,
        (2, 0, 1): 0.1, (2, 1, 1): 0.6, (2, 2, 1): 0.1, (2, 3, 1): 0.1, (2, 4, 1): 0.1,
        (2, 0, 2): 0.1, (2, 1, 2): 0.1, (2, 2, 2): 0.6, (2, 3, 2): 0.1, (2, 4, 2): 0.1,
        (2, 0, 3): 0.1, (2, 1, 3): 0.1, (2, 2, 3): 0.1, (2, 3, 3): 0.6, (2, 4, 3): 0.1,
        (2, 0, 4): 0.1, (2, 1, 4): 0.1, (2, 2, 4): 0.1, (2, 3, 4): 0.1, (2, 4, 4): 0.6,

        # s3, a0        # s3, a1        # s3, a2        # s3, a3        # s3, a4
        (3, 0, 0): 0.6, (3, 1, 0): 0.1, (3, 2, 0): 0.1, (3, 3, 0): 0.1, (3, 4, 0): 0.1,
        (3, 0, 1): 0.1, (3, 1, 1): 0.6, (3, 2, 1): 0.1, (3, 3, 1): 0.1, (3, 4, 1): 0.1,
        (3, 0, 2): 0.1, (3, 1, 2): 0.1, (3, 2, 2): 0.6, (3, 3, 2): 0.1, (3, 4, 2): 0.1,
        (3, 0, 3): 0.1, (3, 1, 3): 0.1, (3, 2, 3): 0.1, (3, 3, 3): 0.6, (3, 4, 3): 0.1,
        (3, 0, 4): 0.1, (3, 1, 4): 0.1, (3, 2, 4): 0.1, (3, 3, 4): 0.1, (3, 4, 4): 0.6,

        # s4, a0        # s4, a1        # s4, a2        # s4, a3        # s4, a4
        (4, 0, 0): 0.6, (4, 1, 0): 0.1, (4, 2, 0): 0.1, (4, 3, 0): 0.1, (4, 4, 0): 0.1,
        (4, 0, 1): 0.1, (4, 1, 1): 0.6, (4, 2, 1): 0.1, (4, 3, 1): 0.1, (4, 4, 1): 0.1,
        (4, 0, 2): 0.1, (4, 1, 2): 0.1, (4, 2, 2): 0.6, (4, 3, 2): 0.1, (4, 4, 2): 0.1,
        (4, 0, 3): 0.1, (4, 1, 3): 0.1, (4, 2, 3): 0.1, (4, 3, 3): 0.6, (4, 4, 3): 0.1,
        (4, 0, 4): 0.1, (4, 1, 4): 0.1, (4, 2, 4): 0.1, (4, 3, 4): 0.1, (4, 4, 4): 0.6,
    }
    # Validate the transition function
    validate_transition(Tr_sas, S, A)
    #
    reward_constants = [  # Reward depends on action and the number of agent same state
        # The first constant is relate to the number of state, another is just constant
        (4, 1),
        (5, 2),
        (7, 2),
        (5, 2),
        (7, 2),
    ];
    assert len(reward_constants) == len(A)

    def R(ds, ai):
        if ds == 0:
            return 0
        actual_reward = reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
        return actual_reward

    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1];
    assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def scG_fiveState_RD():
    seed(SEED_NUM)
    #
    num_agents, S, A = 15, range(5), range(5)
    Tr_sas = {
        # s0, a0        # s0, a1        # s0, a2        # s0, a3        # s0, a4
        (0, 0, 0): 0.6, (0, 1, 0): 0.1, (0, 2, 0): 0.1, (0, 3, 0): 0.1, (0, 4, 0): 0.1,
        (0, 0, 1): 0.1, (0, 1, 1): 0.6, (0, 2, 1): 0.1, (0, 3, 1): 0.1, (0, 4, 1): 0.1,
        (0, 0, 2): 0.1, (0, 1, 2): 0.1, (0, 2, 2): 0.6, (0, 3, 2): 0.1, (0, 4, 2): 0.1,
        (0, 0, 3): 0.1, (0, 1, 3): 0.1, (0, 2, 3): 0.1, (0, 3, 3): 0.6, (0, 4, 3): 0.1,
        (0, 0, 4): 0.1, (0, 1, 4): 0.1, (0, 2, 4): 0.1, (0, 3, 4): 0.1, (0, 4, 4): 0.6,

        # s1, a0        # s1, a1        # s1, a2        # s1, a3        # s1, a4
        (1, 0, 0): 0.6, (1, 1, 0): 0.1, (1, 2, 0): 0.1, (1, 3, 0): 0.1, (1, 4, 0): 0.1,
        (1, 0, 1): 0.1, (1, 1, 1): 0.6, (1, 2, 1): 0.1, (1, 3, 1): 0.1, (1, 4, 1): 0.1,
        (1, 0, 2): 0.1, (1, 1, 2): 0.1, (1, 2, 2): 0.6, (1, 3, 2): 0.1, (1, 4, 2): 0.1,
        (1, 0, 3): 0.1, (1, 1, 3): 0.1, (1, 2, 3): 0.1, (1, 3, 3): 0.6, (1, 4, 3): 0.1,
        (1, 0, 4): 0.1, (1, 1, 4): 0.1, (1, 2, 4): 0.1, (1, 3, 4): 0.1, (1, 4, 4): 0.6,

        # s2, a0        # s2, a1        # s2, a2        # s2, a3        # s2, a4
        (2, 0, 0): 0.6, (2, 1, 0): 0.1, (2, 2, 0): 0.1, (2, 3, 0): 0.1, (2, 4, 0): 0.1,
        (2, 0, 1): 0.1, (2, 1, 1): 0.6, (2, 2, 1): 0.1, (2, 3, 1): 0.1, (2, 4, 1): 0.1,
        (2, 0, 2): 0.1, (2, 1, 2): 0.1, (2, 2, 2): 0.6, (2, 3, 2): 0.1, (2, 4, 2): 0.1,
        (2, 0, 3): 0.1, (2, 1, 3): 0.1, (2, 2, 3): 0.1, (2, 3, 3): 0.6, (2, 4, 3): 0.1,
        (2, 0, 4): 0.1, (2, 1, 4): 0.1, (2, 2, 4): 0.1, (2, 3, 4): 0.1, (2, 4, 4): 0.6,

        # s3, a0        # s3, a1        # s3, a2        # s3, a3        # s3, a4
        (3, 0, 0): 0.6, (3, 1, 0): 0.1, (3, 2, 0): 0.1, (3, 3, 0): 0.1, (3, 4, 0): 0.1,
        (3, 0, 1): 0.1, (3, 1, 1): 0.6, (3, 2, 1): 0.1, (3, 3, 1): 0.1, (3, 4, 1): 0.1,
        (3, 0, 2): 0.1, (3, 1, 2): 0.1, (3, 2, 2): 0.6, (3, 3, 2): 0.1, (3, 4, 2): 0.1,
        (3, 0, 3): 0.1, (3, 1, 3): 0.1, (3, 2, 3): 0.1, (3, 3, 3): 0.6, (3, 4, 3): 0.1,
        (3, 0, 4): 0.1, (3, 1, 4): 0.1, (3, 2, 4): 0.1, (3, 3, 4): 0.1, (3, 4, 4): 0.6,

        # s4, a0        # s4, a1        # s4, a2        # s4, a3        # s4, a4
        (4, 0, 0): 0.6, (4, 1, 0): 0.1, (4, 2, 0): 0.1, (4, 3, 0): 0.1, (4, 4, 0): 0.1,
        (4, 0, 1): 0.1, (4, 1, 1): 0.6, (4, 2, 1): 0.1, (4, 3, 1): 0.1, (4, 4, 1): 0.1,
        (4, 0, 2): 0.1, (4, 1, 2): 0.1, (4, 2, 2): 0.6, (4, 3, 2): 0.1, (4, 4, 2): 0.1,
        (4, 0, 3): 0.1, (4, 1, 3): 0.1, (4, 2, 3): 0.1, (4, 3, 3): 0.6, (4, 4, 3): 0.1,
        (4, 0, 4): 0.1, (4, 1, 4): 0.1, (4, 2, 4): 0.1, (4, 3, 4): 0.1, (4, 4, 4): 0.6,
    }
    # Validate the transition function
    validate_transition(Tr_sas, S, A)
    #
    reward_constants = [  # Reward depends on action and the number of agent same state
        # The first constant is relate to the number of state, another is just constant
        (4, 1),
        (5, 2),
        (7, 2),
        (5, 2),
        (7, 2),
    ];
    assert len(reward_constants) == len(A)

    def R(ds, ai):
        if ds == 0:
            return 0
        actual_reward = reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
        variance = actual_reward * 0.1
        return np.random.uniform(actual_reward - variance, actual_reward + variance)

    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1];
    assert len(ags_S) == num_agents
    return num_agents, S, A, Tr_sas, R, ags_S


def validate_transition(Tr_sas, S, A):
    for _s in S:
        for a in A:
            p_sa = 0
            for s in S:
                p_sa += Tr_sas[_s, a, s]
            assert abs(p_sa - 1) < EPSILON, p_sa


if __name__ == '__main__':
    for rtype in [R_CONSTANT, R_LINEAR, R_INVERSE, R_EXPONENTIAL]:
        for ttype in [T_SIMPLE, T_COMPLEX]:
            for num_agents in range(5, 25, 5):
                for num_states in range(2, 11):
                    problem_generator(num_agents, num_states, rtype, ttype)