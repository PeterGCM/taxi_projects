import __init__
#
from community_analysis.__init__ import charts_dir
from taxi_common.file_handling_functions import get_all_files
from taxi_common.charts import multiple_line_chart
#
import pandas as pd
import numpy as np


def run():
    target_dir = '/Users/JerryHan88/PycharmProjects/taxi_projects/community_analysis/data/gtrips/2009-TH(23)/0901'
    num_com = len(get_all_files(target_dir, '', '.csv'))
    com_fare = {i : [] for i in range(1, num_com + 1)}
    for mm in range(1, 12):
        target_dir = '/Users/JerryHan88/PycharmProjects/taxi_projects/community_analysis/data/gtrips/2009-TH(23)/09%02d' % mm
        assert num_com == len(get_all_files(target_dir, '', '.csv'))
        for i in range(1, num_com + 1):
            df = pd.read_csv('%s/gtrips-G(%d).csv' % (target_dir, i))

            df_gb = df.groupby(['did'])
            com_fare[i].append(np.mean(df_gb.mean()['fare']) / float(100))
    labels, yss = [], []
    for k, v in com_fare.iteritems():
        labels.append('com %d' % k)
        yss.append(v)
    xs = ['09%02d' % mm for mm in range(1, 12)]
    multiple_line_chart((12, 6), '', 'Year and Month (yymm)', 'Average fare (S$)',
                        (xs, 0), yss, labels, 'upper right', '%s/com_avg_fare' % charts_dir)

if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise