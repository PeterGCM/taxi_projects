import __init__
#
from sc_games import ALPH, GAMMA, EPSILON
from sc_games import MAX_ITER_NUM
from sc_games import NUM_SIMULATION, WARMUP_ITER
from problems import scG_twoState, scG_threeState
from handling_distribution import choose_index_wDist
#
from taxi_common.file_handling_functions import check_dir_create
#
import random, csv


def run():
    num_agents, S, A, Tr_sas, R, ags_S = scG_twoState()
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
            for _ds in range(1, num_agents + 1):
                policy[_s, _ds] = [1 / float(len(A)) for _ in A]
        agts_policy.append(policy)
    #
    #
    #
    num_iter = 0
    while True:
        #
        chosen_agent = num_iter % num_agents
        # simulation
        sim_iter = 0
        while sim_iter < WARMUP_ITER:
            single_sim_run(num_agents, S, ags_S, agts_policy, sa_distribution)
            sim_iter += 1
        C_s_ds = [[0 for _ in xrange(num_agents + 1)] for _ in S]
        for _ in xrange(NUM_SIMULATION):
            single_sim_run(num_agents, S, ags_S, agts_policy, sa_distribution)
            ds_ = [0] * len(S)
            for si_ in ags_S:
                ds_[si_] += 1
            #
            for s in S:
                C_s_ds[s][ds_[s]] += 1
        P_s_ds = {}
        delta_s_ds = {}
        P_sds_a_sds = {}
        for _s in S:
            for _ds in xrange(num_agents + 1):
                P_s_ds[_s, _ds] = C_s_ds[_s][_ds] / float(NUM_SIMULATION)
                delta_s_ds[_s, _ds] = P_s_ds[_s, _ds] * (1 / float(len(S)))
                #
        for _s in S:
            for _ds in xrange(num_agents + 1):
                for a in A:
                    for s_ in S:
                        for ds_ in xrange(num_agents + 1):
                            P_sds_a_sds[_s, _ds, a, s_, ds_] = Tr_sas[_s, a, s_] * P_s_ds[s_, ds_]
        # Solve MDPs

        # Update agt policy

        assert False




        num_iter += 1





def single_sim_run(num_agents, S, ags_S, agts_policy, sa_distribution):
    _ds = [0] * len(S)
    for _si in ags_S:
        _ds[_si] += 1
    for i in range(num_agents):
        _si = ags_S[i]
        _dsi = _ds[_si]
        ai = choose_index_wDist(agts_policy[i][_si, _dsi])
        si_ = choose_index_wDist(sa_distribution[_si, ai])
        ags_S[i] = si_



if __name__ == '__main__':
    run()