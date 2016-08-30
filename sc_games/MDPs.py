import __init__
#
from sc_games import taxi_data
from sc_games import ALPH, GAMMA, EPSILON
from sc_games import MAX_ITER_NUM
from sc_games import NUM_SIMULATION, WARMUP_ITER
from problems import scG_twoState, scG_threeState, scG_fiveState, scG_fiveState_RD
from handling_distribution import choose_index_wDist
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
#
import random, csv
from gurobipy import *


def run():
    for prob in [scG_twoState, scG_threeState, scG_fiveState, scG_fiveState_RD]:
        generate_policy(prob)


def generate_policy(prob):
    num_agents, S, A, _, _, _ = prob()
    problem_dir = '%s/%s' % (taxi_data, prob.__name__);
    check_dir_create(problem_dir)
    agts_policy = solve_MDPs(prob)

    as_fpath = '%s/policy-%s.csv' % (problem_dir, 'MDPs')
    ordered_Q_labels = []
    for s in S:
        for ds in xrange(num_agents + 1):
            for a in A:
                ordered_Q_labels.append('Q(%d,%d,%d)' % (s, ds, a))
    with open(as_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_header = ['agent'] + ordered_Q_labels
        writer.writerow(new_header)
    for i, policy in enumerate(agts_policy):
        with open(as_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [i]
            for s in S:
                for ds in xrange(num_agents + 1):
                    for a in A:
                        new_row.append(policy[s, ds][a])
            writer.writerow(new_row)


def solve_MDPs(prob):
    num_agents, S, A, Tr_sas, R, ags_S0 = prob()
    sa_distribution = {}
    for _s in S:
        for a in A:
            sa_distribution[_s, a] = [Tr_sas[_s, a, s_] for s_ in S]
    #
    # Generate a initial policy for each agents
    #
    agts_policy = []
    for _ in range(num_agents):
        policy = {}
        for _s in S:
            for _ds in xrange(num_agents + 1):
                policy[_s, _ds] = [1 / float(len(A)) for _ in A]
        agts_policy.append(policy)
    #
    #
    #
    num_iter = 0
    while True:
        #
        chosen_agent = num_iter % num_agents
        old_policy = agts_policy[chosen_agent]
        # simulation
        sim_iter = 0
        while sim_iter < WARMUP_ITER:
            ags_S = single_sim_run(num_agents, S, ags_S0, agts_policy, sa_distribution)
            sim_iter += 1
        C_s_ds = {(s, ds): 0 for ds in xrange(num_agents + 1) for s in S}
        for _ in xrange(NUM_SIMULATION):
            ags_S = single_sim_run(num_agents, S, ags_S, agts_policy, sa_distribution)
            ds_ = [0] * len(S)
            for si_ in ags_S:
                ds_[si_] += 1
            #
            for s in S:
                C_s_ds[s, ds_[s]] += 1
        P_s_ds = {}
        delta_s_ds = {}
        P_sds_a_sds = {}
        for _s in S:
            for _ds in xrange(num_agents + 1):
                P_s_ds[_s, _ds] = C_s_ds[_s, _ds] / float(NUM_SIMULATION)
                delta_s_ds[_s, _ds] = P_s_ds[_s, _ds] * (1 / float(len(S)))
                #
        for _s in S:
            for _ds in xrange(num_agents + 1):
                for a in A:
                    for s_ in S:
                        for ds_ in xrange(num_agents + 1):
                            P_sds_a_sds[_s, _ds, a, s_, ds_] = Tr_sas[_s, a, s_] * P_s_ds[s_, ds_]
        # Solve MDPs
        m = Model()
        # Add variables
        dv = {}
        for s in S:
            for ds in xrange(num_agents + 1):
                for a in A:
                    dv[s, ds, a] = m.addVar(lb=0.0, name='x(%d,%d,%d)' % (s, ds, a))
        # Process pending updates
        m.update()
        # Set objective function
        obj = LinExpr()
        for s in S:
            for ds in xrange(num_agents + 1):
                for a in A:
                    obj += P_s_ds[s, ds] * R(ds, a) * dv[s, ds, a]
        m.setObjective(obj, GRB.MAXIMIZE);
        # Add constraints
        for _s in S:
            for _ds in xrange(num_agents + 1):
                m.addConstr(quicksum(dv[_s, _ds, a] for a in A)
                            - GAMMA * quicksum(P_sds_a_sds[_s, _ds, a, s_, ds_] * dv[s, ds, a] for a in A for ds_ in xrange(num_agents + 1) for s_ in S)
                            == delta_s_ds[_s, _ds])
        # Solve model
        m.optimize()
        #
        assert m.status == GRB.Status.OPTIMAL, 'Errors while optimization'
        # Generate a new policy
        new_policy = {}
        for s_ in S:
            for ds_ in xrange(num_agents + 1):
                action_sum = sum([dv[s_, ds_, a].X for a in A])
                if action_sum == 0:
                    new_policy[s_, ds_] = [1 / float(len(A)) for _ in A]
                else:
                    new_policy[s_, ds_] = [dv[s_, ds_, a].X / float(action_sum) for a in A]
                assert abs(sum(new_policy[s_, ds_]) - 1.0) < EPSILON
        is_updated = False
        for s in S:
            for ds in xrange(num_agents + 1):
                for a in A:
                    if EPSILON < abs(old_policy[s, ds][a] - new_policy[s, ds][a]):
                        is_updated = True
        agts_policy[chosen_agent] = new_policy
        if not is_updated:
            break
        num_iter += 1
        print num_iter
    # for policy in agts_policy:
    #     print policy
    return agts_policy


def single_sim_run(num_agents, S, ags_S0, agts_policy, sa_distribution):
    ags_S = ags_S0[:]
    _ds = [0] * len(S)
    for _si in ags_S:
        _ds[_si] += 1
    for i in xrange(num_agents):
        _si = ags_S[i]
        _dsi = _ds[_si]
        ai = choose_index_wDist(agts_policy[i][_si, _dsi])
        si_ = choose_index_wDist(sa_distribution[_si, ai])
        ags_S[i] = si_
    return ags_S



if __name__ == '__main__':
    run()