import __init__
#
from __init__ import taxi_data, algo_names
from problems import sc_game0, sc_game1, sc_game2, sc_game3
#
from taxi_common.file_handling_functions import check_path_exist
#
import csv


def run():
    for al in [
              'Qs',
              'Qst',
                ]:
    # for al in algo_names.itervalues():
        for prob in [
                     sc_game0,
                     sc_game1,
                     sc_game2,
                     sc_game3
                     ]:
            num_agents, S, A, _, _, _ = prob()
            _dir = '%s/%s/%s' % (taxi_data, al, prob.__name__)
            fn = '%s/history_%s_%s.csv' % (_dir, al, prob.__name__)
            fn1 = '%s/last_iter_%s_%s.csv' % (_dir, al, prob.__name__)
            if not check_path_exist(fn1):
                with open(fn, 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    last_iter = []
                    for row in reader:
                        if len(last_iter) == num_agents:
                            last_iter = []
                        last_iter.append(row)
                    with open(fn1, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        writer.writerow(headers)
                        for row in last_iter:
                            writer.writerow(row)
            fn2 = '%s/last_policy_%s_%s.csv' % (_dir, al, prob.__name__)
            with open(fn1, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                if len(hid) == len(['iter', 'agent', 'state', 'dist', 'action']) + len(S) * len(A):
                    best_a = {}
                    for row in reader:
                        i = eval(row[hid['agent']])
                        for s in S:
                            max_Q, argmax_a = -1e400, None
                            for a in A:
                                Q_value = eval(row[hid['Q(%d,%d)' % (s, a)]])
                                if max_Q < Q_value:
                                    max_Q, argmax_a = Q_value, a
                            assert -1e400 < max_Q
                            best_a[i, s] = argmax_a
                    with open(fn2, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        new_headers = ['s \ agent']
                        new_headers += ['%d' % i for i in range(num_agents)]
                        new_headers += ['num_a1']
                        writer.writerow(new_headers)
                        for s in S:
                            row = [s]
                            for i in range(num_agents):
                                row.append(best_a[i, s])
                            row += [sum(row[1:])]
                            writer.writerow(row)
                else:
                    assert len(hid) == len(['iter', 'agent', 'state', 'dist', 'action']) + len(S) * num_agents * len(A), hid
                    best_a = {}
                    for row in reader:
                        i = eval(row[hid['agent']])
                        for s in S:
                            for ds in range(1, num_agents + 1):
                                max_Q, argmax_a = -1e400, None
                                for a in A:
                                    Q_value = eval(row[hid['Q(%d,%d,%d)' % (s, ds, a)]])
                                    if max_Q < Q_value:
                                        max_Q, argmax_a = Q_value, a
                                assert -1e400 < max_Q
                                best_a[i, s, ds] = argmax_a

                    with open(fn2, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        new_headers = ['(s, ds) \ agent']
                        new_headers += ['%d' % i for i in range(num_agents)]
                        new_headers += ['num_a1']
                        writer.writerow(new_headers)
                        for s in S:
                            for ds in range(1, num_agents + 1):
                                row = [(s, ds)]
                                for i in range(num_agents):
                                    row.append(best_a[i, s, ds])
                                row += [sum(row[1:])]
                                writer.writerow(row)


if __name__ == '__main__':
    run()