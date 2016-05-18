from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports.handling_pkl import load_picle_file
from supports._setting import for_learning_dir
from supports.etc_functions import get_all_files
#
import csv
#
fn = '%s/results_summary.csv' % (for_learning_dir)
# 
def run():
    dir_path = '/Users/JerryHan88/taxi/full_drivers_trips_q_comparision'
    pickle_files = get_all_files(dir_path, 
                                 'comparision-', '.pkl')
    for pkl_file in pickle_files:
        yymm = pkl_file[:-len('.pkl')].split('-')[-1]
        yy, mm = int(yymm[:2]), int(yymm[2:])
        whole_rev, whole_count, sub_rev, sub_count = load_picle_file('%s/comparision-%s.pkl' % (dir_path, yymm))
        with open(fn, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow([yy, mm, whole_rev / whole_count, sub_rev / sub_count])
    
    
    
    
    
#     with open(fn, 'wt') as w_csvfile:
#         writer = csv.writer(w_csvfile)
#         new_headers = ['ALPHA', 'GAMMA', 'yy', 'mm', 'avg-whole-rev', 'avg-sub-rev']
#         writer.writerow(new_headers)
#     
#     for i in xrange(1, 11): 
#         ALPHA = i / 10 
#         for j in xrange(1, 11):
#             GAMMA = j / 10
#             process_files(ALPHA, GAMMA)
            
def process_files(ALPHA, GAMMA):
    ALPHA_GAMMA_dir = for_learning_dir + '/ALPHA-%.2f-GAMMA-%.2f' % (ALPHA, GAMMA)
    if not os.path.exists(ALPHA_GAMMA_dir):
        return None
    pickle_files = get_all_files(ALPHA_GAMMA_dir, 'ALPHA-%.2f-GAMMA-%.2f' % (ALPHA, GAMMA), '.pkl')
    for pkl_file in pickle_files:
        yymm = pkl_file[:-len('.pkl')].split('-')[-1]
        yy, mm = int(yymm[:2]), int(yymm[2:])
        whole_rev, whole_count, sub_rev, sub_count = load_picle_file('%s/results-%s.pkl' % (ALPHA_GAMMA_dir, yymm))
        with open(fn, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile)
            writer.writerow([ALPHA, GAMMA, yy, mm, whole_rev / whole_count, sub_rev / sub_count])

def draw_chart():
    import pandas as pd
    from supports.charts import line_3D
    df = pd.read_csv('%s/%s' % (for_learning_dir, 'results_summary.csv'))
    df['diff'] = df['avg-sub-rev'] - df['avg-whole-rev']
    gb = df.groupby(['ALPHA', 'GAMMA'])
    xyz = [[] for _ in xrange(10)]
    _alpha, _gamma, _diff = None, None, -1e400
    for alpha, gamma, diff in gb.mean()['diff'].to_frame('avg_diff').reset_index().values:
        print alpha, gamma, diff
        if diff > _diff:
            _alpha, _gamma, _diff = alpha, gamma, diff
        i = int(alpha * 10) - 1
        xyz[i].append([alpha, gamma, diff/100])
    
    line_3D((6, 6), '', r'$\alpha$', r'$\gamma$', 'Difference, S$',xyz)

if __name__ == '__main__':
    run()
#     draw_chart()
