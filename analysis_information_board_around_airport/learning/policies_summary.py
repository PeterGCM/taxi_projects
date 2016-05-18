from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir, for_full_driver_dir
from supports.etc_functions import get_all_files
from supports.handling_pkl import save_pickle_file, load_picle_file
from supports._setting import DAY_OF_WEEK, TIME_SLOTS, IN_AP, OUT_AP

import csv, datetime

index_IN_OUT_AP = {IN_AP:0, OUT_AP:1}
IN_OUT_AP_index = {0:IN_AP, 1:OUT_AP}
#
def drivers():
    policies = {}
    for fn in get_all_files(for_full_driver_dir, 'diff-pin-eco-extreme-drivers-trip-', '.csv'):
        _, _, _, _, _, _, yymm = fn[:-len('.csv')].split('-')
        with open('%s/%s' % (for_full_driver_dir, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            id_ptet, id_ptel = headers.index('prev-trip-end-time'), headers.index('prev-trip-end-location')
            id_sl = headers.index('start-location') 
            for row in reader:
                prev_tetime_datetime = datetime.datetime.fromtimestamp(int(row[id_ptet]))
                s1, s2 = prev_tetime_datetime.strftime("%a"), prev_tetime_datetime.hour
                s3 = row[id_ptel]
                if not policies.has_key((s1, s2, s3)): 
                    policies[(s1, s2, s3)] = [0, 0]
                i = index_IN_OUT_AP[row[id_sl]]
                policies[(s1, s2, s3)][i] += 1
    op_policies = {}
    for k, v in policies.iteritems():
        op_policies[k] = ('%.2f' % (v[0] / (v[0] + v[1])), '%.2f' % (v[1] / (v[0] + v[1])))
    save_pickle_file('extreme_drivers_policy.pkl', op_policies)        

def q_learning():
    policies_dir = for_learning_dir + '/%s' % ('ALPHA-0.10-GAMMA-0.50')
    policies = {}
    for fn in get_all_files(policies_dir, 'ALPHA-', '.pkl'):
        Qsa_value, _ = load_picle_file(policies_dir + '/%s' % fn)
        for s1 in DAY_OF_WEEK:
            for s2 in TIME_SLOTS:
                for s3 in [IN_AP, OUT_AP]:
                    if not policies.has_key((s1, s2, s3)): 
                        policies[(s1, s2, s3)] = [0, 0]
                    i = index_IN_OUT_AP[IN_AP] if Qsa_value[(s1, s2, s3, IN_AP)] >= Qsa_value[(s1, s2, s3, OUT_AP)] else index_IN_OUT_AP[OUT_AP]
                    policies[(s1, s2, s3)][i] += 1
    op_policies = {}
    for k, v in policies.iteritems():
        op_policies[k] = ('%.2f' % (v[0] / (v[0] + v[1])), '%.2f' % (v[1] / (v[0] + v[1])))
    save_pickle_file('q_learning_policy.pkl', op_policies)     

def test():
    extreme_drivers_policy = load_picle_file('extreme_drivers_policy.pkl')
    q_learning_policy = load_picle_file('q_learning_policy.pkl')
    for s1 in DAY_OF_WEEK:
        for s2 in TIME_SLOTS:
            k = (s1, s2, IN_AP)
            if extreme_drivers_policy.has_key(k) and q_learning_policy.has_key(k):
                print k, extreme_drivers_policy[k], q_learning_policy[k]
    print ''
    for s1 in DAY_OF_WEEK:
        for s2 in TIME_SLOTS:
            k = (s1, s2, OUT_AP)
            if extreme_drivers_policy.has_key(k) and q_learning_policy.has_key(k):
                print k, extreme_drivers_policy[k], q_learning_policy[k] 
    
if __name__ == '__main__':
    q_learning()
    drivers()
    test()
