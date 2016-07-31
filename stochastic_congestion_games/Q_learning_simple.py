import __init__

from __init__ import taxi_data
from problems import simple_sc_game0


SEED_NUM = 3
ALPH, GAMMA, EPSILON = .9, .9, .00000001


import random, sys
sys.stdout = open('%s/console_%d.txt' % (taxi_data, SEED_NUM), 'w')


def run():
    num_agents, S, A, Tr_sas, R, ags_S = simple_sc_game0(SEED_NUM)
    #
    # Initialize multi-agents reinforcement learning
    #
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
    iter_count = 0
    history = []
    while True:
        iter_count += 1
        #
        # Agents choose a best action which give the maximum Q-value at their current state
        #
        ags_A = []
        for i in xrange(num_agents):
            r = random.random()
            if r < 0.008:
                #
                # Exploration
                #
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
            s0, ai = ags_S[i], ags_A[i]
            #
            s1 = 0 if random.random() < Tr_sas[s0][ai][0] else 1  # This can be applicable when only two actions are considered
            max_Q_sa = -1e400
            for a1 in A:
                if max_Q_sa < ags_Q_sa[i][s1, a1]:
                    max_Q_sa = ags_Q_sa[i][s1, a1]
            Q_sa0 = ags_Q_sa[i][s0, ai]
            reward = R(i, s0, ags_A)
            ags_Q_sa[i][s0, ai] += ALPH * (reward + GAMMA * max_Q_sa - ags_Q_sa[i][s0, ai])
            #
            # Check convergence
            #
            ags_convergence[i] = True if abs(Q_sa0 - ags_Q_sa[i][s0, ai]) < EPSILON else False
            #
            # State transition
            #
            ags_S[i] = s1

        history.append([iter_count, ags_S, ags_A])
        print iter_count, ags_S, ags_A
        for Q_sa in ags_Q_sa:
            print '\t',
            for s in S:
                for a in A:
                    print (s, a),':','%.4f' % Q_sa[s,a], '  ',
            print ''
            # print '\t' + str(['%s: %.4f' % (str(k), v) for k, v in Q_sa.iteritems()])
        print ''
        if len([w for w in ags_convergence if w]) == num_agents:
            break


if __name__ == '__main__':
    run()