import __init__
#
from __init__ import taxi_data
from __init__ import ALPH, GAMMA, EPSILON
from __init__ import MAX_ITER_NUM
from __init__ import EXPLORE_DURATION
from __init__ import algo_names, get_current_pyname
from problems import sc_game0, sc_game1, sc_game2, sc_game3
#
from taxi_common.file_handling_functions import check_dir_create
#
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
            for i in xrange(1, num_agents + 1):
                for a in A:
                    Q_sa[s, i, a] = 0
        ags_Q_sa.append(Q_sa)
    fn = '%s/history_%s_%s.csv' % (prob_dir, algo_names[get_current_pyname()], problem.__name__)
    with open(fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['iter','agent','state','dist','action']
        for s in S:
            for i in xrange(1, num_agents + 1):
                for a in A:
                    new_headers.append('Q(%d,%d,%d)'%(s, i, a))
        writer.writerow(new_headers)
        for i in xrange(num_agents):
            i_Q_sa = ags_Q_sa[i]
            instance = [iter_count, i, ags_S[i],0, 0]
            for s in S:
                for i in xrange(1, num_agents + 1):
                    for a in A:
                        instance.append(i_Q_sa[s, i, a])
            writer.writerow(instance)
    #
    # Start stochastic congestion games
    #
    while True:
        iter_count += 1
        # current states
        ds = [0] * len(S)
        for si in ags_S:
            ds[si] += 1
        #
        # Agents choose a best action which give the maximum Q-value at their current state
        #
        ags_A = []
        for i in xrange(num_agents):
            r = random.random()
            if iter_count < EXPLORE_DURATION and r < 0.01:
                #
                # Exploration
                #
                random_a = random.choice(A)
                ags_A.append(random_a)
            else:
                si = ags_S[i]
                i_Q_sa = ags_Q_sa[i]
                max_Q_sa, argmax_a = -1e400, None
                for ai in A:
                    if max_Q_sa < i_Q_sa[si, ds[si], ai]:
                        max_Q_sa = i_Q_sa[si, ds[si], ai]
                        argmax_a = ai
                ags_A.append(argmax_a)
        #
        # Simulation for estimate next states
        #
        sim_next_states = []
        for _i in xrange(num_agents):
            sim_next_states.append(0 if random.random() < Tr_sas[ags_S[_i]][ags_A[_i]][0] else 1)
        _ds = [0] * len(S)
        for _s in sim_next_states:
            _ds[_s] += 1
        #
        # Update Q-values
        #
        ags_convergence = [False] * num_agents
        for i0 in xrange(num_agents):
            si, ai, _si = ags_S[i0], ags_A[i0], sim_next_states[i0]
            Q_sa0 = i_Q_sa[si, ds[si], ai]
            max_Q_sa = -1e400
            i_Q_sa = ags_Q_sa[i0]
            for _ai in A:
                if max_Q_sa < i_Q_sa[_si, _ds[_si], _ai]:
                    max_Q_sa = i_Q_sa[_si, _ds[_si], _ai]
            reward = R(si, ai, ds[si])
            i_Q_sa[si, ds[si], ai] += ALPH * (reward + GAMMA * max_Q_sa - i_Q_sa[si, ds[si], ai])
            ags_convergence[i0] = True if abs(Q_sa0 - i_Q_sa[si, ds[si], ai]) < EPSILON else False
            ags_S[i0] = _si
            #
            # Save history
            #
            with open(fn, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                instance = [iter_count, i0, si, ds[si], ai]
                for s in S:
                    for i in xrange(1, num_agents + 1):
                        for a in A:
                            instance.append(i_Q_sa[s, i, a])
                writer.writerow(instance)
        #
        # Check convergence
        #
        if len([w for w in ags_convergence if w]) == num_agents or iter_count == MAX_ITER_NUM:
            break


if __name__ == '__main__':
    for prob in [
                 # sc_game0,
                 # sc_game1,
                 # sc_game2,
                 sc_game3
                 ]:
        run(prob)