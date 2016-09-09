import __init__
#
from sc_games import taxi_data
#
from taxi_common.file_handling_functions import get_all_directories, get_all_files
from taxi_common.charts import multiple_line_chart
#
import csv

SAMPLING_INTERVAL = 100
DRAW_SAMPLED_CHART = True

def run():
    problem_dn = 'P0-G(5)-S(2)-R(L)-Tr(S)'
    problem_dpath = '%s/%s' % (taxi_data, problem_dn)
    for dn in get_all_directories(problem_dpath):
        dpath = '%s/%s' % (problem_dpath, dn)
        policy_fns = set(get_all_files(dpath, '', 'dist.csv'))
        # Q-values
        for fn in get_all_files(dpath, '', '.csv'):
            if fn in policy_fns:
                continue
            print fn
            fpath = '%s/%s' % (dpath, fn)
            with open(fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                q_labels = [k for k in hid.iterkeys() if k not in ['iter','s', 'ds', 'a', 'reward']]
                q_labels.sort()
                chart_fpath = '%s/%s' % (dpath, fn[:-len('.csv')])
                xs, yss = [], [[] for _ in q_labels]
                for row in reader:
                    xs.append('')
                    for i, l in enumerate(q_labels):
                        yss[i].append(eval(row[hid[l]]))
                new_xs, new_yss = [], [[] for _ in q_labels]
                for i in xrange(len(xs)):
                    if i % SAMPLING_INTERVAL == 0:
                        new_xs.append('')
                        for j in xrange(len(q_labels)):
                            new_yss[j].append(yss[j][i])
                if DRAW_SAMPLED_CHART:
                    drawing_xs, drawing_yss = new_xs, new_yss
                else:
                    drawing_xs, drawing_yss = xs, yss
                multiple_line_chart((12, 6), '', 'Iteration', 'Value',
                                    (drawing_xs, 0), drawing_yss, q_labels, 'upper left', chart_fpath)
        # Policy
        for fn in policy_fns:
            fpath = '%s/%s' % (dpath, fn)
            with open(fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                q_labels = [k for k in hid.iterkeys() if k not in ['iter', 's', 'ds', 'a', 'reward']]
                q_labels.sort()
                chart_fpath = '%s/%s' % (dpath, fn[:-len('.csv')])
                xs, yss = [], [[] for _ in q_labels]
                for row in reader:
                    xs.append('')
                    for i, l in enumerate(q_labels):
                        yss[i].append(eval(row[hid[l]]))
                new_xs, new_yss = [], [[] for _ in q_labels]
                for i in xrange(len(xs)):
                    if i % SAMPLING_INTERVAL == 0:
                        new_xs.append('')
                        for j in xrange(len(q_labels)):
                            new_yss[j].append(yss[j][i])
                if DRAW_SAMPLED_CHART:
                    drawing_xs, drawing_yss = new_xs, new_yss
                else:
                    drawing_xs, drawing_yss = xs, yss
                multiple_line_chart((12, 6), '', 'Iteration', 'Probability',
                                    (drawing_xs, 0), drawing_yss, q_labels, 'upper left', chart_fpath)






if __name__ == '__main__':
    run()