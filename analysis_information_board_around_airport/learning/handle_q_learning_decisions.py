from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir
from supports.logger import logging_msg
from supports.handling_pkl import save_pickle_file, load_picle_file
from supports._setting import IN_AP, OUT_AP
from supports._setting import DAY_OF_WEEK, TIME_SLOTS
from supports.etc_functions import get_all_files, get_all_directories
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime
#
HOUR = 60 * 60
MOD_STAN = 100000
#
def run():
    candi_dirs = get_all_directories(for_learning_dir)
    q_lerning_ended_dir = [dn for dn in candi_dirs if len(get_all_files(for_learning_dir + '/%s' % (dn), 'ALPHA-', '.pkl')) == 22]
    init_multiprocessor()
    counter = 0
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
#             process_files(yymm, q_lerning_ended_dir)
            put_task(process_files, [yymm, q_lerning_ended_dir])
            counter += 1
    end_multiprocessor(counter)
                
def process_files(yymm, q_lerning_ended_dir):
    candi_pkl_files = []
    for dn in q_lerning_ended_dir:
        if os.path.exists('%s/%s/results-%s.pkl' % (for_learning_dir, dn, yymm)):
            continue
        candi_pkl_files.append('%s/%s/%s-q-value-fare-dur-%s.pkl' % (for_learning_dir, dn, dn, yymm))
    result_pkls = [os.path.dirname(pkl_path) + '/results-%s.pkl'% yymm for pkl_path in candi_pkl_files]
    #
    list_argmax_as = []
    state_action_fare_dur = None
    for pkl_file_path in candi_pkl_files:
        Qsa_value, state_action_fare_dur = load_picle_file(pkl_file_path)
        argmax_as = {}
        for s1 in DAY_OF_WEEK:
            for s2 in TIME_SLOTS:
                for s3 in [IN_AP, OUT_AP]:
                    argmax_as[(s1, s2, s3)] = IN_AP if Qsa_value[(s1, s2, s3, IN_AP)] >= Qsa_value[(s1, s2, s3, OUT_AP)] else OUT_AP
        list_argmax_as.append(argmax_as)
    #
    whole_rev, whole_count = 0, 0
    list_sub_rev, list_sub_count = [0 for _ in xrange(len(candi_pkl_files))], [0 for _ in xrange(len(candi_pkl_files))]
    
    count = 0        
    with open('%s/whole-trip-%s.csv' % (for_learning_dir, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_prev_tetime, id_prev_teloc = headers.index('prev-trip-end-time'), headers.index('prev-trip-end-location')
        id_stime, id_sloc = headers.index('start-time'), headers.index('start-location'),
        id_dur, id_fare = headers.index('duration'), headers.index('fare')
        for row in reader:
            prev_tetime, stime = eval(row[id_prev_tetime]), eval(row[id_stime]) 
            setup_time = stime - prev_tetime
            #
            prev_tetime_datetime = datetime.datetime.fromtimestamp(prev_tetime)
            s1, s2 = prev_tetime_datetime.strftime("%a"), prev_tetime_datetime.hour
            s3 = row[id_prev_teloc]
            #
            a = row[id_sloc]
            #
            dur, fare = eval(row[id_dur]), eval(row[id_fare])
            alter_a = OUT_AP if a == IN_AP else IN_AP
            if state_action_fare_dur[(s1, s2, s3, alter_a)][1] == 0:
                op_cost = 0
            else:
                op_cost = (setup_time + dur) * state_action_fare_dur[(s1, s2, s3, alter_a)][0] / state_action_fare_dur[(s1, s2, s3, alter_a)][1] 
            economic_profit = fare - op_cost
            #
            whole_rev += economic_profit
            whole_count += 1
            
            for i, argmax_as in enumerate(list_argmax_as):
                if argmax_as[(s1, s2, s3)] == a:
                    list_sub_rev[i] += economic_profit
                    list_sub_count[i] += 1
            count += 1
            if count % MOD_STAN == 0:
                print '%s, %d' % (yymm, count)
                logging_msg('%s, %d' % (yymm, count))
                for i in xrange(len(result_pkls)):
                    result_fn = result_pkls[i]
                    save_pickle_file(result_fn, [whole_rev, whole_count, list_sub_rev[i], list_sub_count[i]])
    for i in xrange(len(result_pkls)):
        result_fn = result_pkls[i]
        save_pickle_file(result_fn, [whole_rev, whole_count, list_sub_rev[i], list_sub_count[i]])
        
if __name__ == '__main__':
    run()
