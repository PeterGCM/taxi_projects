import __init__
#
from __init__ import taxi_data, algo_names
from __init__ import MAX_ITER_NUM
from problems import sc_game0, sc_game1, sc_game2, sc_game3
#
from taxi_common.file_handling_functions import check_path_exist, save_pickle_file, load_pickle_file
#
import csv
import numpy as np


def run():
    for al in [
              # 'Qs',
              'Qst',
                ]:
    # for al in algo_names.itervalues():
        for prob in [
                     # sc_game0,
                     # sc_game1,
                     # sc_game2,
                     sc_game3
                     ]:
            num_agents, S, A, Tr_sas, R, ags_S = prob()
            _dir = '%s/%s/%s' % (taxi_data, al, prob.__name__)
            policies_fn = '%s/polices_%s_%s.csv' % (_dir, al, prob.__name__)
            # if check_path_exist(policies_fn):
            #     policies = load_pickle_file(policies_fn)
            # else:
            policies = []
            for i in range(num_agents):
                #
                fn = '%s/agent%d_adist_%s_%s.csv' % (_dir, i, al, prob.__name__)
                agent_policy = {}
                with open(fn, 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    hid = {h: i for i, h in enumerate(headers)}
                    last_row = None
                    for row in reader:
                        last_row = row
                    if len(hid) == len(['iter', 'state', 'dist', 'action']) + len(S) * len(A):
                        for _s in S:
                            agent_policy[_s] = [eval(last_row[hid['D(%d,%d)' % (_s, _a)]]) for _a in A]
                    else:
                        assert len(hid) == len(['iter', 'state', 'dist', 'action']) + len(S) * num_agents * len(A), hid
                        for _s in S:
                            for _ds in xrange(1, num_agents + 1):
                                agent_policy[_s, _ds] = [eval(last_row[hid['D(%d,%d,%d)' % (_s, _ds, _a)]]) for _a in A]
                policies.append(agent_policy)
            # save_pickle_file(policies_fn, policies)
            #
            experiment_fn = '%s/experiment_%s_%s.csv' % (_dir, al, prob.__name__)
            with open(experiment_fn, 'wb') as w_csvfile:
                writer = csv.writer(w_csvfile)
                new_headers = ['iter']
                for i in xrange(num_agents):
                    new_headers += ['agt%d-state' % i, 'agt%d-ds' % i,
                                    'agt%d-action' % i, 'agt%d-reward' % i,
                                    'agt%d-avg-reward' % i]
                new_headers += ['current-total-reward', 'avg-total-reard']
                writer.writerow(new_headers)
            num_agents, S, A, Tr_sas, R, ags_S
            #
            # Simulation
            #
            ags_reward_sum = [0] * num_agents
            total_reward_sum = 0
            for num_iter in range(1, MAX_ITER_NUM):
                ds = [0] * len(S)
                for si in ags_S:
                    ds[si] += 1
                ags_A, cur_ags_reward = [], []
                new_row = [num_iter]
                for i in xrange(num_agents):
                    i_policy = policies[i]
                    si = ags_S[i]
                    chosen_a = None
                    if len(hid) == len(['iter', 'state', 'dist', 'action']) + len(S) * len(A):
                        poly_dist = i_policy[si]
                        chosen_a = np.random.choice(len(A), 1, poly_dist)
                    else:
                        assert len(hid) == len(['iter', 'state', 'dist', 'action']) + len(S) * num_agents * len(A), hid
                        poly_dist = i_policy[si, ds[si]]
                        chosen_a = np.random.choice(len(A), 1, poly_dist)
                    reward = R(si, chosen_a, ds[si])
                    ags_reward_sum[i] += reward
                    new_row += [si, ds[si], chosen_a, reward, ags_reward_sum[i] / float(num_iter)]
                    #
                    ags_A.append(chosen_a)
                    cur_ags_reward.append(reward)
                cur_total_reward = sum(cur_ags_reward)
                total_reward_sum += cur_total_reward
                new_row += [cur_total_reward, total_reward_sum/ float(num_iter)]
                #
                with open(experiment_fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow(new_row)


if __name__ == '__main__':
    from traceback import format_exc

    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise