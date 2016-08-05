import __init__
#
from __init__ import taxi_data

from taxi_common.charts import multiple_line_chart
from taxi_common.charts import line_3D
#
import csv


fn = '%s/sc_game1_seed(3).csv' % taxi_data
#
# state
#
ags_S_num = []
iter_counter = set()
UNIT = 1000
with open(fn, 'rb') as r_csvfile:
    reader = csv.reader(r_csvfile)
    headers = reader.next()
    hid = {h: i for i, h in enumerate(headers)}
    fn1 = '%s/sc_game1_seed(3)_summary.csv' % taxi_data
    with open(fn1, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        new_headers = ['iter','state','action']
        writer.writerow(new_headers)
    for row in reader:
        iter_num = eval(row[hid['iter']])
        if iter_num not in iter_counter:
            iter_counter.add(iter_num)
            ags_S_num.append([0] * 2)
        ags_S_num[-1][eval(row[hid['action']])] += 1
        if iter_num != 0 and iter_num % UNIT == 0 and sum(ags_S_num[-1]) == 10:
            print 'start arrange'
            xyz = []
            for i, x in enumerate(ags_S_num):
                _iter = i + (iter_num / UNIT - 1) * UNIT
                xyz.append([_iter] + x)
                with open(fn1, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow([_iter, x, x])
            line_3D((12, 6), '', 'iteration', 'a0', 'a1', xyz, taxi_data + '/fig_%d' % (iter_num / UNIT -1))
            # line_3D((12, 6), '', 'iteration', 'a0', 'a1', xyz)
            ags_S_num = []
    # line_3D((18, 6), '', 'iteration', 'a0', 'a1', xyz)
print 'finish arrangement'

