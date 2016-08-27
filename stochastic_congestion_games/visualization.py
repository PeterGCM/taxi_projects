import __init__
#

from taxi_common.charts import multiple_line_chart
from taxi_common.charts import line_3D
#
import csv

_dir = '/Users/JerryHan88/PycharmProjects/taxi_projects/stochastic_congestion_games/data_20160826/Qs/sc_game1'
_Q = _dir.split('/')[-2]
_prob = _dir.split('/')[-1]
fn = '%s/history.csv' % _dir
#
# state
#
ags_S_num, ags_A_num = [], []
iter_counter = set()
UNIT = 1000
with open(fn, 'rb') as r_csvfile:
    reader = csv.reader(r_csvfile)
    headers = reader.next()
    hid = {h: i for i, h in enumerate(headers)}
    fn1 = '%s/summary_%s_%s.csv' % (_dir, _Q, _prob)
    with open(fn1, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['iter','state','action']
        writer.writerow(new_headers)
    for row in reader:
        iter_num = eval(row[hid['iter']])
        if iter_num not in iter_counter:
            iter_counter.add(iter_num)
            ags_S_num.append([0] * 2)
            ags_A_num.append([0] * 2)
        ags_S_num[-1][eval(row[hid['state']])] += 1
        ags_A_num[-1][eval(row[hid['action']])] += 1
        if iter_num != 0 and iter_num % UNIT == 0 and sum(ags_A_num[-1]) == 5:
            print 'start arrange'
            s_xyz, a_xyz = [], []
            for i, a_dist in enumerate(ags_A_num):
                _iter = i + (iter_num / UNIT - 1) * UNIT
                s_dist = ags_S_num[i]
                s_xyz.append([_iter] + s_dist)
                a_xyz.append([_iter] + a_dist)
                with open(fn1, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([_iter, s_dist, a_dist])
            line_3D((12, 6), '', 'iteration', 's0', 's1', s_xyz, '%s/%s_%s_s_%d' % (_dir, _Q, _prob, iter_num / UNIT -1))
            line_3D((12, 6), '', 'iteration', 'a0', 'a1', a_xyz, '%s/%s_%s_a_%d' % (_dir, _Q, _prob, iter_num / UNIT -1))
            ags_S_num, ags_A_num = [], []
print 'finish arrangement'

