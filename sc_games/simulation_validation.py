import __init__
#
from sc_games import taxi_data
from sc_games import MAX_ITER_NUM
from problems import scG_twoState, scG_threeState, scG_fiveState, scG_fiveState_RD
from handling_distribution import choose_index_wDist
#
from taxi_common.file_handling_functions import get_all_files
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, random


def run():
    # init_multiprocessor(11)
    # count_num_jobs = 0

    for prob in [scG_twoState, scG_threeState, scG_fiveState, scG_fiveState_RD]:
        problem_dir = '%s/%s' % (taxi_data, prob.__name__);
        num_agents, S, A, _, _, _ = prob()
        for policy_fn in get_all_files(problem_dir, 'policy', 'csv'):
            # if policy_fn in ['policy-MDPs.csv', 'policy-pure-normal-agents.csv']:
            #     continue
            print policy_fn
            approach_name = policy_fn[len('policy-'):-len('.csv')]
            policies = []
            fpath = '%s/%s' % (problem_dir, policy_fn)
            is_sensitive = False
            with open(fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                if len(hid) == len(['agent']) + (num_agents + 1) * len(S) * len(A):
                    is_sensitive = True
                    for row in reader:
                        policy = {}
                        for s in S:
                            for ds in xrange(num_agents + 1):
                                policy[s, ds] = [eval(row[hid['Q(%d,%d,%d)' % (s, ds, a)]]) for a in A]
                        policies.append(policy)
                else:
                    is_sensitive = False
                    for row in reader:
                        policy = {}
                        for s in S:
                            policy[s] = [eval(row[hid['Q(%d,%d)' % (s, a)]]) for a in A]
                        policies.append(policy)
            experiment(prob, problem_dir, approach_name, is_sensitive, policies)
    #         put_task(experiment, [prob, problem_dir, approach_name, is_sensitive, policies])
    #         count_num_jobs += 1
    # end_multiprocessor(count_num_jobs)


def experiment(prob, problem_dir, approach_name, is_sensitive, policies):
    num_agents, S, A, Tr_sas, R, ags_S = prob()
    sa_distribution = {}
    for _s in S:
        for a in A:
            sa_distribution[_s, a] = [Tr_sas[_s, a, s_] for s_ in S]
    #
    experiment_fpath = '%s/experiment_%s.csv' % (problem_dir, approach_name)
    with open(experiment_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        new_headers = ['iter']
        for i in xrange(num_agents):
            new_headers += ['agt%d-s' % i, 'agt%d-ds' % i,
                            'agt%d-a' % i, 'agt%d-reward' % i,
                            'agt%d-avg-reward' % i]
        new_headers += ['current-total-reward', 'avg-total-reard']
        writer.writerow(new_headers)
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
                if not is_sensitive:
                    poly_dist = i_policy[si]
                else:
                    assert is_sensitive
                    poly_dist = i_policy[si, ds[si]]
                if sum(poly_dist) == 0:
                    chosen_a == random.randrange(len(poly_dist))
                else:
                    chosen_a = choose_index_wDist(poly_dist)
                reward = R(ds[si], chosen_a)
                ags_reward_sum[i] += reward
                new_row += [si, ds[si], chosen_a, reward, ags_reward_sum[i] / float(num_iter)]
                #
                ags_A.append(chosen_a)
                cur_ags_reward.append(reward)
            cur_total_reward = sum(cur_ags_reward)
            total_reward_sum += cur_total_reward
            new_row += [cur_total_reward, total_reward_sum / float(num_iter)]
            #
            with open(experiment_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(new_row)

            for i in xrange(num_agents):
                _si = ags_S[i]
                ai = ags_A[i]
                si_ = choose_index_wDist(sa_distribution[_si, ai])
                ags_S[i] = si_


if __name__ == '__main__':
    run()