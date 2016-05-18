from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir
from supports._setting import DAY_OF_WEEK, TIME_SLOTS, IN_AP, OUT_AP
from supports.handling_pkl import load_picle_file
from supports.charts import grid_charts, one_grid_chart
#
id_dow = {dow : i for i, dow in enumerate(DAY_OF_WEEK)}

def run():
    op_policies_q_learning = load_picle_file('/Users/JerryHan88/git/workspace_SMU/taxi_py/learning/q_learning_policy.pkl') 
    op_policies_ext_drivers = load_picle_file('/Users/JerryHan88/git/workspace_SMU/taxi_py/learning/extreme_drivers_policy.pkl')
    
    decision_inAP_Q, decision_outAP_Q = [], []
    decision_inAP_D, decision_outAP_D = [], []
    for s1 in DAY_OF_WEEK:
        for s2 in TIME_SLOTS:
            for s3 in [IN_AP, OUT_AP]:
                p_IN_AP, p_OUT_AP = op_policies_q_learning[(s1, s2, s3)]
                max_a_Q = IN_AP if eval(p_IN_AP) >= eval(p_OUT_AP) else OUT_AP
                c = 0 if max_a_Q == IN_AP else 1
                if s3 == IN_AP:
                    decision_inAP_Q.append([s1, s2, c])
                else:
                    decision_outAP_Q.append([s1, s2, c])
                #
                try:
                    p_IN_AP, p_OUT_AP = op_policies_ext_drivers[(s1, s2, s3)]
                    max_a_D = IN_AP if eval(p_IN_AP) >= eval(p_OUT_AP) else OUT_AP
                    c = 0 if max_a_D == IN_AP else 1
                except KeyError:
                    c = 2
                    print s1, s2, s3
                if s3 == IN_AP:
                    decision_inAP_D.append([s1, s2, c])
                else:
                    decision_outAP_D.append([s1, s2, c])
    inAP_Q = [(s2, id_dow[s1], a) for s1, s2, a in decision_inAP_Q]
    outAP_Q = [(s2, id_dow[s1], a) for s1, s2, a in decision_outAP_Q]
    inAP_D = [(s2, id_dow[s1], a) for s1, s2, a in decision_inAP_D]
    outAP_D = [(s2, id_dow[s1], a) for s1, s2, a in decision_outAP_D]
    
    d = [inAP_Q, outAP_Q, inAP_D, 
         outAP_D]
    
    n = ['decision_inAP_Q', 'decision_outAP_Q', 'decision_inAP_D', 
         'decision_outAP_D']
    for i in xrange(4):
        one_grid_chart(('Time slot', []), ('', DAY_OF_WEEK), ['Go to AP', 'Go to OA'], '', d[i], n[i])
    
def process_files(yymm):
#     Qsa_value, _ = load_picle_file('%s/q-value-fare-dur-%s.pkl' % (for_learning_dir, yymm))
    Qsa_value, _ = load_picle_file('/Users/JerryHan88/taxi/for_learning/ALPHA-0.70-GAMMA-0.30/ALPHA-0.70-GAMMA-0.30-q-value-fare-dur-0904.pkl')
    decision_inAP, decision_outAP = [], []
    for s1 in DAY_OF_WEEK:
        for s2 in TIME_SLOTS:
            for s3 in [IN_AP, OUT_AP]:
#                 print (s1, s2, s3), Qsa_value[(s1, s2, s3, IN_AP)], Qsa_value[(s1, s2, s3, OUT_AP)]
                max_a = IN_AP if Qsa_value[(s1, s2, s3, IN_AP)] >= Qsa_value[(s1, s2, s3, OUT_AP)] else OUT_AP
                c = 0 if max_a == IN_AP else 1
                if s3 == IN_AP:
                    decision_inAP.append([s1, s2, c])
                else:
                    decision_outAP.append([s1, s2, c])
    for s1, s2, a in decision_inAP:
        print 'inAP', s1, s2, a
    for s1, s2, a in decision_outAP:
        print 'outAP', s1, s2, a  
    _data = [
             [(s2, id_dow[s1], a) for s1, s2, a in decision_inAP],
             [(s2, id_dow[s1], a) for s1, s2, a in decision_outAP]
             ]
#     titles = ['Decision in the airport', 'Decision outside of the airport']
#     grid_charts(('24 Time slots', []), ('', DAY_OF_WEEK), ['In Airport', 'Out Airport'], titles, _data, '%s/q-value-fare-dur-%s.pdf' % (for_learning_dir, yymm))
    one_grid_chart(('Time slot', []), ('', DAY_OF_WEEK), ['In Airport', 'Out Airport'], '', [(s2, id_dow[s1], a) for s1, s2, a in decision_inAP], 'decision_inAP_q_e')
    
    
if __name__ == '__main__':
    run()
#     process_files('')
