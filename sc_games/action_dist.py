import __init__
#
from __init__ import taxi_data
from problems import sc_game0, sc_game1, sc_game2, sc_game3

import csv


def run():
    for al in [
        'Qs',
        # 'Qst',
    ]:
        for prob in [
            # sc_game0,
            # sc_game1,
            # sc_game2,
            sc_game3
        ]:
            num_agents, S, A, _, _, _ = prob()
            _dir = '%s/%s/%s' % (taxi_data, al, prob.__name__)
            fn = '%s/history_%s_%s.csv' % (_dir, al, prob.__name__)

            agt_action_count = []
            for i in range(num_agents):
                C_sa = {}
                # for s in S:
                #     for ds in xrange(1, num_agents + 1):
                #         for a in A:
                #             C_sa[s, ds, a] = 0

                for s in S:
                    for a in A:
                        C_sa[s, a] = 0

                agt_action_count.append(C_sa)
                #
                fn1 = '%s/agent%d_adist_%s_%s.csv' % (_dir, i, al, prob.__name__)
                fn2 = '%s/agent%d_adist_simple_%s_%s.csv' % (_dir, i, al, prob.__name__)
                with open(fn1, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    new_headers = ['iter', 'state', 'dist', 'action']
                    # for s in S:
                    #     for ds in xrange(1, num_agents + 1):
                    #         for a in A:
                    #             new_headers.append('D(%d,%d,%d)' % (s, ds, a))
                    for s in S:
                        for a in A:
                            new_headers.append('D(%d,%d)' % (s, a))


                    writer.writerow(new_headers)
                with open(fn2, 'wt') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    new_headers = ['iter', 'state', 'dist', 'action']
                    # for s in S:
                    #     for ds in xrange(1, num_agents + 1):
                    #         new_headers.append('D(%d,%d)' % (s, ds))

                    for s in S:
                        new_headers.append('D(%d)' % (s))

                    writer.writerow(new_headers)
            with open(fn, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    _iter = eval(row[hid['iter']])
                    if _iter == 0:
                        continue
                    i = eval(row[hid['agent']])
                    s, ds, a = eval(row[hid['state']]), eval(row[hid['dist']]), eval(row[hid['action']])
                    # agt_action_count[i][s, ds, a] += 1
                    agt_action_count[i][s, a] += 1
                    #
                    fn1 = '%s/agent%d_adist_%s_%s.csv' % (_dir, i, al, prob.__name__)
                    fn2 = '%s/agent%d_adist_simple_%s_%s.csv' % (_dir, i, al, prob.__name__)
                    with open(fn1, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        new_row = [_iter, s, ds, a]
                        # for _s in S:
                        #     for _ds in xrange(1, num_agents + 1):
                        #         state_count = 0
                        #         for _a in A:
                        #             state_count += agt_action_count[i][_s, _ds, _a]
                        #         for _a in A:
                        #             if state_count == 0:
                        #                 new_row.append(0)
                        #             else:
                        #                 new_row.append(agt_action_count[i][_s, _ds, _a] / float(state_count))

                        for _s in S:
                            state_count = 0
                            for _a in A:
                                state_count += agt_action_count[i][_s, _a]
                            for _a in A:
                                if state_count == 0:
                                    new_row.append(0)
                                else:
                                    new_row.append(agt_action_count[i][_s, _a] / float(state_count))
                        writer.writerow(new_row)
                    with open(fn2, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        new_row = [_iter, s, ds, a]
                        # for _s in S:
                        #     for _ds in xrange(1, num_agents + 1):
                        #         state_count = 0
                        #         for _a in A:
                        #             state_count += agt_action_count[i][_s, _ds, _a]
                        #         if state_count == 0:
                        #             new_row.append(0)
                        #         else:
                        #             da0 = agt_action_count[i][_s, _ds, 0] / float(state_count)
                        #             da1 = agt_action_count[i][_s, _ds, 1] / float(state_count)
                        #             new_row.append(da0 - da1)

                        for _s in S:
                            state_count = 0
                            for _a in A:
                                state_count += agt_action_count[i][_s, _a]
                            if state_count == 0:
                                new_row.append(0)
                            else:
                                da0 = agt_action_count[i][_s, 0] / float(state_count)
                                da1 = agt_action_count[i][_s, 1] / float(state_count)
                                new_row.append(da0 - da1)
                        writer.writerow(new_row)



if __name__ == '__main__':
    run()