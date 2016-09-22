import __init__
#
from sc_games import taxi_data
from sc_games import ALPH, GAMMA, MAX_ITER_NUM, BIG_M
from sc_games import PAR_L_ID_NUM_AGENT, PAR_L_ID_NUM_STATE, PAR_L_ID_DS
from sc_games import SH_PARAMETER, SH_REWARD, SH_TRANSITION
from sc_games import T_SIMPLE, T_COMPLEX
from sc_games import sheet_names

from handling_distribution import choose_index_wDist
#
from taxi_common.file_handling_functions import check_dir_create, get_parent_dir, \
                                                get_fn_only, get_all_files, check_path_exist, get_all_directories
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, xlrd


def run():
    # init_multiprocessor(6)
    # count_num_jobs = 0
    # for prob in [scG_twoState, scG_threeState, scG_fiveState, scG_fiveState_RD]:
    #     for agent_type, dir_name in [(normal_agent, 'pure-normal-agents'), (sensitive_agent, 'pure-sensitive-agents')]:
    #         num_agents, S, A, _, _, _ = prob()
    #         problem_dir = '%s/%s' % (taxi_data, prob.__name__); check_dir_create(problem_dir)
    #         put_task(multi_processors_instance, [prob, dir_name, agent_type])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)
    init_multiprocessor(11)
    count_num_jobs = 0
    for problem_dn in get_all_directories(taxi_data):
        # problem_dn = 'P1-G(10)-S(3)-R(I)-Tr(C)'
        problem_dpath = '%s/%s' % (taxi_data, problem_dn)
        problem_fpath = '%s/%s.xls' % (problem_dpath, problem_dn)
        workbook = xlrd.open_workbook(problem_fpath)
        par_sheet = workbook.sheet_by_name(sheet_names[SH_PARAMETER])
        num_agents = int(par_sheet.cell(PAR_L_ID_NUM_AGENT, 1).value)
        num_states = int(par_sheet.cell(PAR_L_ID_NUM_STATE, 1).value)
        S, A = range(num_states), range(num_states)
        ags_S = list(eval(par_sheet.cell(PAR_L_ID_DS, 1).value))
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
                s0, ds0, a, s1, v = (transition_sheet.cell(i, j).value for j in [hid['s0'], hid['ds0'], hid['a'], hid['s1'], hid['Tr']])
                s0, ds0, a, s1 = map(int, [s0, ds0, a, s1])
                Tr[s0, ds0, a, s1] = v
        problem_inputs = [num_agents, S, A, R, Tr, ags_S, transition_type]
        sol_dpath = '%s/%s' % (problem_dpath, 'pn-agents')
        #
        # multi_processors_instance(problem_inputs, sol_dpath, normal_agent)
        put_task(multi_processors_instance, [problem_inputs, sol_dpath, normal_agent])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def multi_processors_instance(problem_inputs, sol_dpath, agent_class):
    num_agents, S, A, _, _, _, _ = problem_inputs
    check_dir_create(sol_dpath)
    agents = [agent_class(sol_dpath, i, S, A, num_agents) for i in xrange(num_agents)]
    start_learning(problem_inputs, agents)
    generate_policy(sol_dpath)


def start_learning(problem_inputs, agents):
    print 'start learning'
    num_agents, S, A, R, Tr, ags_S, transition_type = problem_inputs
    #
    aggregated_dist = {}
    if transition_type == T_SIMPLE:
        for s0 in S:
            for a in A:
                aggregated_dist[s0, a] = [Tr[s0, a, s1] for s1 in S]
    else:
        assert transition_type == T_COMPLEX
        for s0 in S:
            for ds0 in xrange(num_agents + 1):
                for a in A:
                    aggregated_dist[s0, ds0, a] = [Tr[s0, ds0, a, s1] for s1 in S]
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
            ds0 = _ds[_si]
            if transition_type == T_SIMPLE:
                s = choose_index_wDist(aggregated_dist[_si, ai])
            else:
                assert transition_type == T_COMPLEX
                s = choose_index_wDist(aggregated_dist[_si, ds0, ai])
            next_states.append(s)
        ds_ = [0] * len(S)
        for si_ in next_states:
            ds_[si_] += 1
        #
        # Update Q-values
        #
        for i in xrange(num_agents):
            _si, ai, si_ = ags_S[i], ags_A[i], next_states[i]
            agents[i].update_record_Q_value(_si, _ds[_si], ai, si_, ds_[si_], R[_ds[_si], ai])
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
            writer = csv.writer(w_csvfile, lineterminator='\n')
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
            writer = csv.writer(w_csvfile, lineterminator='\n')
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
            for i in xrange(num_agents + 1):
                for a in A:
                    self.Q_sa[s, i, a] = BIG_M
        self.iter_num = 0
        problem_name = hr_dir.split('/')[-1]
        self.hr_fpath = '%s/%s-sensitive-agent%d.csv' % (hr_dir, problem_name, agt_id)
        with open(self.hr_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['iter', 's', 'ds', 'a', 'reward']
            for s in S:
                for i in xrange(num_agents + 1):
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
                for ds in xrange(self.num_agents + 1):
                    for a in self.A:
                        instance.append(self.Q_sa[s, ds, a])
            writer.writerow(instance)


def generate_policy(hr_dir):
    parent_dir = get_parent_dir(hr_dir)
    approach_name = get_fn_only(hr_dir)
    as_fpath = '%s/policy-%s.csv' % (parent_dir, approach_name)
    for agt_history_fn in get_all_files(hr_dir, '', '.csv'):
        agt_dist_fpath = '%s/%s-dist.csv' % (hr_dir, agt_history_fn[:-len('.csv')])
        agt_id = eval(agt_history_fn[:-len('.csv')].split('-')[-1][len('agent'):])
        #
        with open('%s/%s' % (hr_dir, agt_history_fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            Q_labels = [k for k in hid.iterkeys() if k.startswith('Q')]
            is_normal_agent = True if len(eval(Q_labels[0][len('Q'):])) == 2 else False
            state_space, action_space = set(), set()
            ordered_Q_labels = []
            C_sa = {}
            if is_normal_agent:
                for Ql in Q_labels:
                    s, a = map(eval, Ql[len('Q('):-len(')')].split(','))
                    state_space.add(s)
                    action_space.add(a)
                state_space, action_space = sorted(list(state_space)), sorted(list(action_space))
                for s in state_space:
                    for a in action_space:
                        ordered_Q_labels.append('Q(%d,%d)' % (s, a))
                        C_sa[s, a] = 0
            else:
                for Ql in Q_labels:
                    s, ds, a = map(eval, Ql[len('Q('):-len(')')].split(','))
                    state_space.add((s, ds))
                    action_space.add(a)
                state_space, action_space = sorted(list(state_space)), sorted(list(action_space))
                for s, ds in state_space:
                    for a in action_space:
                        ordered_Q_labels.append('Q(%d,%d,%d)' % (s, ds, a))
                        C_sa[(s, ds), a] = 0
            #
            last_row = None
            with open(agt_dist_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_header = ['iter'] + ordered_Q_labels
                writer.writerow(new_header)
                for row in reader:
                    _iter = eval(row[hid['iter']])
                    s, ds, a = eval(row[hid['s']]), eval(row[hid['ds']]), eval(row[hid['a']])
                    css = s if is_normal_agent else (s, ds)
                    C_sa[css, a] += 1
                    #
                    new_row = [_iter]
                    for s in state_space:
                        state_count = 0
                        for a in action_space:
                            state_count += C_sa[s, a]
                        for a in action_space:
                            if state_count == 0:
                                new_row.append(0)
                            else:
                                new_row.append(C_sa[s, a] / float(state_count))
                    writer.writerow(new_row)
                    last_row = new_row
        if not check_path_exist(as_fpath):
            with open(as_fpath, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_header = ['agent'] + ordered_Q_labels
                writer.writerow(new_header)
        last_row.pop(0)
        with open(as_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [agt_id] + last_row
            writer.writerow(new_row)


if __name__ == '__main__':
    run()