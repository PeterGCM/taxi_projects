import sc_games
#
from sc_games import SEED_NUM, EPSILON
#
from random import seed


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
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (8, 2),
                        (12, 5)]; assert len(reward_constants) == len(A)
    R = lambda ds, ai : reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1]; assert len(ags_S) == num_agents
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
    reward_constants = [ # Reward depends on action and the number of agent same state
                         # The first constant is relate to the number of state, another is just constant
                        (4, 1),
                        (5, 2),
                        (7, 2),
                ];assert len(reward_constants) == len(A)

    def R(ds, ai):
        actual_reward = reward_constants[ai][0] / float(ds) + reward_constants[ai][1]
        return actual_reward

    ags_S = [0, 1, 1, 0, 1, 1, 0, 1, 1, 1];
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
    scG_threeState()