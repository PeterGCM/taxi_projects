import sc_games
#
from sc_games import taxi_data
from sc_games import ALPH, GAMMA, MAX_ITER_NUM, BIG_M
from problems import scG_twoState, scG_threeState
from handling_distribution import choose_index_wDist
#
from taxi_common.file_handling_functions import check_dir_create
#
import csv


def run():
    num_agents, S, A, _, _, _ = scG_twoState()
    # hr_dir = '%s_%s' % ('%s/%s' % (taxi_data, scG_twoState.__name__), 'pAgent'); check_dir_create(hr_dir)
    # agents = [normal_agent(hr_dir, i, S, A) for i in xrange(num_agents)]
    hr_dir = '%s_%s' % ('%s/%s' % (taxi_data, scG_twoState.__name__), 'psAgent');
    check_dir_create(hr_dir)
    agents = [sensitive_agent(hr_dir, i, S, A, num_agents) for i in xrange(num_agents)]
    #
    start_learning(scG_twoState, agents)


def start_learning(problem, agents):
    num_agents, S, A, Tr_sas, R, ags_S = problem()
    #
    sa_distribution = {}
    for _si in S:
        for a in A:
            sa_distribution[_si, a] = [Tr_sas[_si, a, s] for s in S]
    #
    # Start stochastic congestion games
    #
    iter_count = 0
    while True:
        iter_count += 1
        # current states
        _ds = [0] * len(S)
        for _si in ags_S:
            _ds[_si] += 1
        #
        # Agents choose a best action which give the maximum Q-value at their current state
        #
        ags_A = []
        for i in xrange(num_agents):
            _si = ags_S[i]
            ags_A.append(agents[i].choose_bestA(_si, _ds[_si]))
        #
        # Simulation for estimate next states
        #
        next_states = []
        for i in xrange(num_agents):
            _si, ai = ags_S[i], ags_A[i]
            s = choose_index_wDist(sa_distribution[_si, ai])
            next_states.append(s)
        ds_ = [0] * len(S)
        for si_ in next_states:
            ds_[si_] += 1
        #
        # Update Q-values
        #
        for i in xrange(num_agents):
            _si, ai, si_ = ags_S[i], ags_A[i], next_states[i]
            agents[i].update_record_Q_value(_si, _ds[_si], ai, si_, ds_[si_], R(_ds[_si], ai))
            ags_S[i] = si_
        #
        if iter_count == MAX_ITER_NUM:
            break


class normal_agent(object):
    def __init__(self, hr_dir, agt_id, S, A, num_agents=None):
        self.agt_id = agt_id
        self.S, self.A = S, A
        self.Q_sa = {}
        for s in S:
            for a in A:
                self.Q_sa[s, a] = BIG_M
        #
        self.iter_num = 0
        problem_name = hr_dir.split('/')[-1]
        self.hr_fpath = '%s/%s-normal-agent%d.csv' % (hr_dir, problem_name, agt_id)
        with open(self.hr_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['iter', 's', 'ds', 'a', 'reward']
            for s in S:
                for a in A:
                    new_headers.append('Q(%d,%d)' % (s, a))
            writer.writerow(new_headers)

    def choose_bestA(self, si, _):
        max_Q_sa, argmax_a = -1e400, None
        for ai in self.A:
            if max_Q_sa < self.Q_sa[si, ai]:
                max_Q_sa = self.Q_sa[si, ai]
                argmax_a = ai
        return argmax_a

    def update_record_Q_value(self, _si, _dsi, ai, si_, _, reward):
        max_Q_sa = -1e400
        for ai_ in self.A:
            if max_Q_sa < self.Q_sa[si_, ai_]:
                max_Q_sa = self.Q_sa[si_, ai_]
        self.Q_sa[_si, ai] += ALPH * (reward + GAMMA * max_Q_sa - self.Q_sa[_si, ai])
        # Save history
        self.iter_num += 1
        with open(self.hr_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile)
            instance = [self.iter_num, _si, _dsi, ai, reward]
            for s in self.S:
                for a in self.A:
                    instance.append(self.Q_sa[s, a])
            writer.writerow(instance)


class sensitive_agent(object):
    def __init__(self, hr_dir, agt_id, S, A, num_agents):
        self.agt_id = agt_id
        self.S, self.A, self.num_agents = S, A, num_agents
        self.Q_sa = {}
        for s in S:
            for i in xrange(1, num_agents + 1):
                for a in A:
                    self.Q_sa[s, i, a] = BIG_M
        self.iter_num = 0
        problem_name = hr_dir.split('/')[-1]
        self.hr_fpath = '%s/%s-sensitive-agent%d.csv' % (hr_dir, problem_name, agt_id)
        with open(self.hr_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile)
            new_headers = ['iter', 's', 'ds', 'a', 'reward']
            for s in S:
                for i in xrange(1, num_agents + 1):
                    for a in A:
                        new_headers.append('Q(%d,%d,%d)' % (s, i, a))
            writer.writerow(new_headers)

    def choose_bestA(self, si, dsi):
        max_Q_sa, argmax_a = -1e400, None
        for ai in self.A:
            if max_Q_sa < self.Q_sa[si, dsi, ai]:
                max_Q_sa = self.Q_sa[si, dsi, ai]
                argmax_a = ai
        return argmax_a

    def update_record_Q_value(self, _si, _dsi, ai, si_, dsi_, reward):
        max_Q_sa = -1e400
        for ai_ in self.A:
            if max_Q_sa < self.Q_sa[si_, dsi_, ai_]:
                max_Q_sa = self.Q_sa[si_, dsi_, ai_]
        self.Q_sa[_si, _dsi, ai] += ALPH * (reward + GAMMA * max_Q_sa - self.Q_sa[_si, _dsi, ai])
        # Save history
        self.iter_num += 1
        with open(self.hr_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            instance = [self.iter_num, _si, _dsi, ai, reward]
            for s in self.S:
                for ds in xrange(1, self.num_agents + 1):
                    for a in self.A:
                        instance.append(self.Q_sa[s, ds, a])
            writer.writerow(instance)


if __name__ == '__main__':
    run()