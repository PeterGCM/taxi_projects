import __init__
#
from __init__ import taxi_data, algo_names
from problems import sc_game0, sc_game1, sc_game2, sc_game3
#
from taxi_common.file_handling_functions import check_path_exist
#
import csv
#


def run():
    for al in algo_names.itervalues():
        for prob in [sc_game0, sc_game1, sc_game2, sc_game3]:
            num_agents, _, _, _, _, _ = prob()
            _dir = '%s/%s/%s' % (taxi_data, al, prob.__name__)
            fn = '%s/history.csv' % _dir
            fn1 = '%s/last_iteration.csv' % _dir
            if not check_path_exist(fn1):
                with open(fn, 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    last_iter = []
                    for row in reader:
                        if len(last_iter) == num_agents:
                            last_iter = []
                        elif len(last_iter) < num_agents:
                            last_iter.append(row)
                    with open(fn1, 'wt') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        writer.writerow(headers)

if __name__ == '__main__':
    run()