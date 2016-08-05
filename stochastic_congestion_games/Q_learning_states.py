import __init__

from __init__ import taxi_data
from problems import sc_game0, sc_game1, sc_game2, sc_game3

from __init__ import ALPH, GAMMA, EPSILON
from __init__ import MAX_ITER_NUM
from __init__ import EXPLORE_DURATION
from __init__ import algo_names, get_current_pyname

from taxi_common.file_handling_functions import check_dir_create

import random, csv

def run(problem):
    num_agents, S, A, Tr_sas, R, ags_S = problem()
    algo_dir = '%s/%s' % (taxi_data, algo_names[get_current_pyname()]); check_dir_create(algo_dir)
    prob_dir = '%s/%s' % (algo_dir, problem.__name__); check_dir_create(prob_dir)
    #
    # Initialize multi-agents reinforcement learning
    #
    iter_count = 0
    ags_Q_sa = []
    for _ in xrange(num_agents):
        Q_sa = {}
        for s in S:
            for a in A:
                for i in xrange(num_agents + 1):
                    Q_sa[s, a, i] = 0
        ags_Q_sa.append(Q_sa)
    fn = '%s/history.csv' % (prob_dir)
    with open(fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['iter','agent','state','action']
        for s in S:
            for a in A:
                for i in xrange(num_agents + 1):
                    new_headers.append('Q(%d,%d,%d)'%(s, a, i))
        writer.writerow(new_headers)
        for i in xrange(num_agents):
            i_Q_sa = ags_Q_sa[i]
            instance = [iter_count, i, ags_S[i], 0]
            for s in S:
                for a in A:
                    for i in xrange(num_agents + 1):
                        instance.append(i_Q_sa[s, a, i])
            writer.writerow(instance)
    #
    # Start stochastic congestion games
    #
    while True:
        iter_count += 1
        #
        # Agents choose a best action which give the maximum Q-value at their current state
        #
        ags_A = []
        for i in xrange(num_agents):
            r = random.random()
            if iter_count < EXPLORE_DURATION and r < 0.008:
                #
                # Exploration
                #
                random_a = random.choice(A)
                ags_A.append(random_a)
            else:
                # TODO
                #    1. consider max_Q_sa   or maxmin_Q_sa ??   (currently, just max_Q_sa)
                si = ags_S[i]
                i_Q_sa = ags_Q_sa[i]
                max_Q_sa, argmax_a = -1e400, None
                for ai in A:
                    for i1 in xrange(num_agents + 1):
                        if max_Q_sa < i_Q_sa[si, ai, i1]:
                            max_Q_sa = i_Q_sa[si, ai, i1]
                            argmax_a = ai
                ags_A.append(argmax_a)
        #
        # Count the number of state of agents
        #
        # current states
        num_cur_state = [0] * len(S)
        for s0 in ags_S:
            num_cur_state[s0] += 1
        # next states
        next_states = []
        for i, max_ai in enumerate(ags_A):
            s1 = 0 if random.random() < Tr_sas[ags_S[i]][max_ai][0] else 1
            next_states.append(s1)
        num_next_state = [0] * len(S)
        for s1 in next_states:
            num_next_state[s1] += 1
        #
        # Update Q-values
        #
        ags_convergence = [False] * num_agents
        for i0 in xrange(num_agents):
            s0, ai = ags_S[i0], ags_A[i0]
            num_s0 = num_cur_state[s0]
            s1 = next_states[i0]
            num_s1 = num_next_state[s1]
            max_Q_sa = -1e400
            i_Q_sa = ags_Q_sa[i0]
            for a1 in A:
                if max_Q_sa < i_Q_sa[s1, a1, num_s1]:
                    max_Q_sa = i_Q_sa[s1, a1, num_s1]
            Q_sa0 = i_Q_sa[s0, ai, num_s0]
            reward = R(i0, s0, ags_A)
            i_Q_sa[s0, ai, num_s0] += ALPH * (reward + GAMMA * max_Q_sa - i_Q_sa[s0, ai, num_s0])
            #
            # Check convergence
            #
            ags_convergence[i0] = True if abs(Q_sa0 - i_Q_sa[s0, ai, num_s0]) < EPSILON else False
            #
            # State transition
            #
            ags_S[i0] = s1
            #
            # Save history
            #
            with open(fn, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                instance = [iter_count, i0, s0, ai]
                for s in S:
                    for a in A:
                        for i in xrange(num_agents + 1):
                            instance.append(i_Q_sa[s, a, i])
                writer.writerow(instance)
        #
        if len([w for w in ags_convergence if w]) == num_agents or iter_count == MAX_ITER_NUM:
            break


if __name__ == '__main__':
    for prob in [sc_game0, sc_game1, sc_game2, sc_game3]:
        run(prob)