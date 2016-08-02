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
                for i in xrange(num_agents):
                    Q_sa[s, a, i + 1] = 0
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
                # TODO
                #    2. consider max_Q_sa   or maxmin_Q_sa ??   (currently, just max_Q_sa)
                si = ags_S[i]
                max_Q_sa, argmax_a = -1e400, None
                for ai in A:
                    for i1 in xrange(num_agents):
                        if max_Q_sa < i_Q_sa[s1, ai, i1 + 1]:
                            max_Q_sa = i_Q_sa[s1, ai, i1 + 1]
                            argmax_a = ai
                ags_A.append(argmax_a)
        #
        # Count the number of action of agents
        #
        num_same_actions = [0] * len(A)
        for a in ags_A:
            num_same_actions[a] += 1
        #
        # Update Q-values
        #
        ags_convergence = [False] * num_agents
        for i0 in xrange(num_agents):
            s0, ai = ags_S[i0], ags_A[i0]
            s1 = 0 if random.random() < Tr_sas[s0][ai][0] else 1  # This can be applicable when only two actions are considered
            num_ai_actions = num_same_actions[ai]
            # TODO
            # Discuss this part with Prof. Pradeep
            #    1. num_ai_actions   is can be considered as dynamic state defining
            #    2. consider max_Q_sa   or maxmin_Q_sa ??   (currently, just max_Q_sa)
            #
            max_Q_sa = -1e400
            i_Q_sa = ags_Q_sa[i]
            for a1 in A:
                for i1 in xrange(num_agents):
                    if max_Q_sa < i_Q_sa[s1, a1, i1 + 1]:
                        max_Q_sa = i_Q_sa[s1, a1, i1 + 1]
            Q_sa0 = i_Q_sa[s0, ai, num_ai_actions]
            reward = R(i0, s0, ags_A)
            i_Q_sa[s0, ai, num_ai_actions] += ALPH * (reward + GAMMA * max_Q_sa - i_Q_sa[s0, ai, num_ai_actions])
            #
            # Check convergence
            #
            ags_convergence[i] = True if abs(Q_sa0 - i_Q_sa[s0, ai, num_ai_actions]) < EPSILON else False
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