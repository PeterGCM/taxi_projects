import __init__

import random

def sc_problem0():
    #
    # Define a problem
    #
    num_agents, S, A = 3, range(2), range(2)
    Tr_sas = [
               [[.2, .8], # s0 = 0
                [.3, .7]],
               [[.5, .5], # s0 = 1
                [.7, .3]]
             ]
    r1 = [   # r1 is a reward function depending on state and action
           [3, 3], # s = 0
           [3, 3], # s = 1
         ]
    r2_const = [2, 2]
    r2 = lambda a, num_a: r2_const[a] / float(num_a)  # r2 is a reward function depending on agents' action
    R = lambda i, si, ags_A: r1[si][ags_A[i]] + r2(ags_A[i], len([a for a in ags_A if ags_A[i] == a]))
    #
    # Initialize multiagents reinforcement learning
    #
    ALPH, GAMMA, EPSILON = .9, .9, .00000001
    ags_S = [0, 1, 1]
    ags_Q_sa = []
    for _ in xrange(num_agents):
        Q_sa = {}
        for s in S:
            for a in A:
                Q_sa[s, a] = 0
        ags_Q_sa.append(Q_sa)
    #
    # Start stochastic congestion games
    #
    while True:
        #
        # Agents choose a best action which give the maximum Q-value at their current state
        #
        ags_A = []
        for i in xrange(num_agents):
            r = random.random()
            if r < 0.008:
                random_a = random.choice(A)
                ags_A.append(random_a)
            else:
                si = ags_S[i]
                max_Q_sa, argmax_a = -1e400, None
                for ai in A:
                    if max_Q_sa < ags_Q_sa[i][si, ai]:
                        max_Q_sa = ags_Q_sa[i][si, ai]
                        argmax_a = ai
                ags_A.append(argmax_a)
        #
        # Update Q-values
        #
        ags_convergence = [False] * num_agents
        for i in xrange(num_agents):
            si, ai = ags_S[i], ags_A[i]
            exp_Q_value = 0
            for s1 in S:
                max_Q_sa = -1e400
                for a1 in A:
                    if max_Q_sa < ags_Q_sa[i][s1, a1]:
                        max_Q_sa = ags_Q_sa[i][s1, a1]
                exp_Q_value += Tr_sas[si][ai][s1] * max_Q_sa
            Q_sa0 = ags_Q_sa[i][si, ai]
            reward = R(i, si, ags_A)
            ags_Q_sa[i][si, ai] += ALPH * (reward + GAMMA * exp_Q_value - ags_Q_sa[i][si, ai])
            #
            # Check convergence
            #
            ags_convergence[i] = True if abs(Q_sa0 - ags_Q_sa[i][si, ai]) < EPSILON else False
            #
            # State transition
            #
            ags_S[i] = 0 if random.random() < Tr_sas[si][ai][0] else 1

        print ags_A, ags_Q_sa
        if len([w for w in ags_convergence if w]) == num_agents:
            break


if __name__ == '__main__':
    sc_problem0()