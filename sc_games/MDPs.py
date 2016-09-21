import __init__
#
from sc_games import taxi_data
from sc_games import PAR_L_ID_NUM_AGENT, PAR_L_ID_NUM_STATE, PAR_L_ID_DS
from sc_games import SH_PARAMETER, SH_REWARD, SH_TRANSITION
from sc_games import T_SIMPLE, T_COMPLEX
from sc_games import sheet_names
from sc_games import NUM_SIMULATION, WARMUP_ITER
from sc_games import GAMMA, EPSILON
from sc_games import MAX_ITER_NUM
#
from handling_distribution import choose_index_wDist
#
from taxi_common.file_handling_functions import check_dir_create, check_path_exist
#
import csv, xlrd
from gurobipy import *

def run():
    problem_dn = 'P0-G(5)-S(2)-R(L)-Tr(S)'
    problem_dpath = '%s/%s' % (taxi_data, problem_dn)
    problem_fpath = '%s/%s.xls' % (problem_dpath, problem_dn)
    workbook = xlrd.open_workbook(problem_fpath)
    par_sheet = workbook.sheet_by_name(sheet_names[SH_PARAMETER])
    num_agents = int(par_sheet.cell(PAR_L_ID_NUM_AGENT, 1).value)
    num_states = int(par_sheet.cell(PAR_L_ID_NUM_STATE, 1).value)
    S, A = range(num_states), range(num_states)
    ags_S0 = list(eval(par_sheet.cell(PAR_L_ID_DS, 1).value))
    #
    reward_sheet = workbook.sheet_by_name(sheet_names[SH_REWARD])
    R = {}
    for i in range(1, reward_sheet.nrows):
        ds, a, v = (reward_sheet.cell(i, j).value for j in xrange(reward_sheet.ncols))
        ds, a = map(int, [ds, a])
        R[ds, a] = v
    #
    Tr = {}
    transition_sheet = workbook.sheet_by_name(sheet_names[SH_TRANSITION])
    headers = transition_sheet.row_values(0)
    hid = {h: i for i, h in enumerate(headers)}
    if transition_sheet.ncols == len(['s0', 'a', 's1', 'Tr']):
        transition_type = T_SIMPLE
        for i in range(1, transition_sheet.nrows):
            s0, a, s1, v = (transition_sheet.cell(i, j).value for j in [hid['s0'], hid['a'], hid['s1'], hid['Tr']])
            s0, a, s1 = map(int, [s0, a, s1])
            Tr[s0, a, s1] = v
    else:
        assert transition_sheet.ncols == len(['s0', 'ds0', 'a', 's1', 'Tr'])
        transition_type = T_COMPLEX
        #
        for i in range(1, transition_sheet.nrows):
            s0, ds0, a, s1, v = (transition_sheet.cell(i, j).value for j in
                                 [hid['s0'], hid['ds0'], hid['a'], hid['s1'], hid['Tr']])
            s0, ds0, a, s1 = map(int, [s0, ds0, a, s1])
            Tr[s0, ds0, a, s1] = v
    sol_dpath = '%s/%s' % (problem_dpath, 'MDP-agents')
    check_dir_create(sol_dpath)
    if transition_type == T_SIMPLE:
        agents = [TS_MDP_agent(sol_dpath, i, S, A, num_agents) for i in xrange(num_agents)]
    else:
        transition_type == T_COMPLEX
        agents = [TC_MDP_agent(sol_dpath, i, S, A, num_agents) for i in xrange(num_agents)]
    #
    num_iter = 0
    while True:
        ags_S = ags_S0[:]
        chosen_agent = agents[num_iter % num_agents]
        is_updated = chosen_agent.update_policy(ags_S, agents)
        if not is_updated or num_iter < MAX_ITER_NUM:
            break


class TC_MDP_agent(object):
    def __init__(self, hr_dir, agt_id, S, A, R, Tr, num_agents):
        self.agt_id = agt_id
        self.S, self.A, self.R, self.Tr = S, A, R, Tr
        self.iter_num = 0
        problem_name = hr_dir.split('/')[-1]
        self.hr_fpath = '%s/%s-MDP-agent%d.csv' % (hr_dir, problem_name, agt_id)
        new_headers = ['iter']
        self.sa_distribution, self.policy = {}, {}
        for s in S:
            for i in xrange(num_agents + 1):
                for a in A:
                    new_headers.append('P(%d,%d,%d)' % (s, i, a))
                    self.sa_distribution[s, i, a] = [self.Tr[s, i, a, s_] for s_ in S]
                    self.policy[s, i] = [1 / float(len(A)) for _ in A]
        with open(self.hr_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(new_headers)

    def simulation(self, ags_S, agents):
        _ds = [0] * len(self.S)
        for _si in ags_S:
            _ds[_si] += 1
        for i, agt in enumerate(agents):
            _si, _dsi = ags_S[i], _ds[_si]
            ai = choose_index_wDist(agt.policy[_si, _dsi])
            si_ = choose_index_wDist(agt.sa_distribution[_si, _dsi, ai])
            ags_S[i] = si_
        return ags_S

    def update_policy(self, ags_S, agents):
        # Simulation
        sim_iter = 0
        while sim_iter < WARMUP_ITER:
            ags_S = self.simulation(ags_S, agents)
            sim_iter += 1
        C_s_ds = {(s, i): 0 for i in xrange(len(agents) + 1) for s in self.S}
        for _ in xrange(NUM_SIMULATION):
            ags_S = self.simulation(ags_S, agents)
            i_ = [0] * len(self.S)
            for si_ in ags_S:
                i_[si_] += 1
            #
            for s in self.S:
                C_s_ds[s, i_[s]] += 1
        # Estimate parameters
        delta_s_ds, P_s_ds, P_sds_a_sds = {}, {}
        _ds = [0] * len(self.S)
        for _si in ags_S:
            _ds[_si] += 1
        for s in self.S:
            for i in xrange(len(agents) + 1):
                delta_s_ds[s, i] = _ds[s] / float(len(agents))
                P_s_ds[s, i] = C_s_ds[s, i] / float(NUM_SIMULATION)
        for _s in self.S:
            for _i in xrange(len(agents) + 1):
                for a in self.A:
                    for s_ in self.S:
                        for i_ in xrange(len(agents) + 1):
                            P_sds_a_sds[_s, _i, a, s_, i_] = self.Tr[_s, _i, a, s_] * P_s_ds[s_, i_]
        # Solve MDPs
        m = Model()
        # Add variables
        dv = {}
        for s in self.S:
            for i in xrange(len(agents) + 1):
                for a in self.A:
                    dv[s, i, a] = m.addVar(lb=0.0, name='x(%d,%d,%d)' % (s, i, a))
        # Process pending updates
        m.update()
        # Set objective function
        obj = LinExpr()
        for s in self.S:
            for i in xrange(len(agents) + 1):
                for a in self.A:
                    obj += P_s_ds[s, i] * self.R(i, a) * dv[s, i, a]
        m.setObjective(obj, GRB.MAXIMIZE);
        # Add constraints
        for _s in self.S:
            for _i in xrange(len(agents) + 1):
                m.addConstr(quicksum(dv[_s, _i, a] for a in self.A)
                            - GAMMA * quicksum(P_sds_a_sds[_s, _i, a, s_, i_] * dv[s, _i, a]
                                               for a in self.A for i_ in xrange(len(agents) + 1) for s_ in self.S)
                            == delta_s_ds[_s, _i])
        # Solve model
        m.optimize()
        #
        assert m.status == GRB.Status.OPTIMAL, 'Errors while optimization'
        # Generate a new policy
        new_policy = {}
        for s_ in self.S:
            for i_ in xrange(len(agents) + 1):
                action_sum = sum([dv[s_, i_, a].X for a in self.A])
                if action_sum == 0:
                    new_policy[s_, i_] = [1 / float(len(self.A)) for _ in self.A]
                else:
                    new_policy[s_, i_] = [dv[s_, i_, a].X / float(action_sum) for a in self.A]
                assert abs(sum(new_policy[s_, i_]) - 1.0) < EPSILON
        # Record policy and check convergence
        is_updated = False
        new_row = [self.iter_num]
        for s in self.S:
            for ds in xrange(len(agents) + 1):
                for a in self.A:
                    if EPSILON < abs(self.policy[s, i][s, ds][a] - new_policy[s, ds][a]):
                        is_updated = True
                    new_row.append(new_policy[s, ds][a])
        with open(self.hr_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(new_row)
        self.policy = new_policy
        self.iter_num += 1
        return is_updated


class TS_MDP_agent(object):
    def __init__(self, hr_dir, agt_id, S, A, R, Tr, num_agents=None):
        self.agt_id = agt_id
        self.S, self.A, self.R, self.Tr = S, A, R, Tr
        self.iter_num = 0
        problem_name = hr_dir.split('/')[-1]
        self.hr_fpath = '%s/%s-MDP-agent%d.csv' % (hr_dir, problem_name, agt_id)
        new_headers = ['iter']
        self.sa_distribution, self.policy = {}, {}
        for s in S:
            for a in A:
                new_headers.append('P(%d,%d)' % (s, a))
                self.sa_distribution[s, a] = [self.Tr[s, a, s_] for s_ in S]
                self.policy[s] = [1 / float(len(A)) for _ in A]
        with open(self.hr_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(new_headers)

    def simulation(self, ags_S, agents):
        _ds = [0] * len(self.S)
        for _si in ags_S:
            _ds[_si] += 1
        for i, agt in enumerate(agents):
            _si = ags_S[i]
            ai = choose_index_wDist(agt.policy[_si])
            si_ = choose_index_wDist(agt.sa_distribution[_si, ai])
            ags_S[i] = si_
        return ags_S

    def update_policy(self, other_agts_policy):
        pass




if __name__ == '__main__':
    run()