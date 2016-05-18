from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir
from supports._setting import DAY_OF_WEEK, TIME_SLOTS
from supports._setting import HOUR
from supports._setting import IN_AP, OUT_AP
from supports.handling_pkl import save_pickle_file, load_picle_file
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from supports.etc_functions import remove_creat_dir
from supports.logger import logging_msg
#
import csv, datetime
#
MOD_STAN = 100000
#
def run():
#     task_list = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (4, 10), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (6, 10), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (8, 10), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10)]
    init_multiprocessor()
    counter = 0
#     for i, j in task_list:
#         ALPHA = i / 10
#         GAMMA = j / 10
        
    for ALPHA, GAMMA in [(0.3, 0.7),(0.3, 0.9),(0.5, 0.1),(0.5, 0.3),(0.5, 0.8),(0.5, 1.0)]:
        put_task(process_files, [ALPHA, GAMMA])
        counter += 1
    end_multiprocessor(counter)     
#     for i in range(1,11,2):
# #     for i in range(9,0,-2): 
#         ALPHA = i / 10 
#         for j in range(1,11,2):
# #         for j in range(9,0,-2):
#             GAMMA = j / 10
# #             process_files(ALPHA, GAMMA)
#             put_task(process_files, [ALPHA, GAMMA])
#             counter += 1
#     end_multiprocessor(counter)
    
def process_files(ALPHA, GAMMA):
    ALPHA_GAMMA_dir = for_learning_dir + '/ALPHA-%.2f-GAMMA-%.2f' % (ALPHA, GAMMA)
    remove_creat_dir(ALPHA_GAMMA_dir)
    #
    for y in xrange(9, 11):
        for m in xrange(1, 13):
            yymm = '%02d%02d' % (y, m) 
            if yymm in ['0912', '1010']:
                continue
            process_file(ALPHA, GAMMA, ALPHA_GAMMA_dir, yymm)

def process_file(ALPHA, GAMMA, ALPHA_GAMMA_dir, yymm):            
    print 'handle the file; %s' % yymm
    logging_msg('handle the file; %s' % yymm)
    #
    print yymm
    if yymm == '0901':
        prev_yymm = None
    elif yymm == '1001':
        prev_yymm = '0911'
    elif yymm == '1011':
        prev_yymm = '1009'
    else:
        yy, mm = int(yymm[:2]), int(yymm[2:]) 
        prev_yymm = '%02d%02d' % (yy, mm - 1)
    #
    if not prev_yymm:
        Qsa_value, state_action_fare_dur = {}, {}
        locations = [IN_AP, OUT_AP]
        actions = [IN_AP, OUT_AP]
        for s1 in DAY_OF_WEEK:
            for s2 in TIME_SLOTS:
                for s3 in locations:
                    for a in actions:
                        Qsa_value[(s1, s2, s3, a)] = 0
                        state_action_fare_dur[(s1, s2, s3, a)] = [0, 0]
    else:
        Qsa_value, state_action_fare_dur = load_picle_file('%s/ALPHA-%.2f-GAMMA-%.2f-q-value-fare-dur-%s.pkl' % (ALPHA_GAMMA_dir, ALPHA, GAMMA, prev_yymm))
    #
    
    with open('%s/whole-trip-%s.csv' % (for_learning_dir, yymm), 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        id_prev_tetime, id_prev_teloc = headers.index('prev-trip-end-time'), headers.index('prev-trip-end-location')
        id_stime, id_sloc = headers.index('start-time'), headers.index('start-location'),
        id_etime, id_eloc = headers.index('end-time'), headers.index('end-location'),
        id_dur, id_fare = headers.index('duration'), headers.index('fare')
        #
        count = 0
        for row in reader:
            prev_tetime, stime, etime = eval(row[id_prev_tetime]), eval(row[id_stime]), eval(row[id_etime]) 
            setup_time = stime - prev_tetime
            #
            if setup_time < 0 or HOUR * 2 < setup_time:
                continue 
            #
            prev_tetime_datetime = datetime.datetime.fromtimestamp(prev_tetime)
            s1, s2 = prev_tetime_datetime.strftime("%a"), prev_tetime_datetime.hour
            s3 = row[id_prev_teloc]
            #
            etime_datetime = datetime.datetime.fromtimestamp(etime)
            new_s1, new_s2 = etime_datetime.strftime("%a"), etime_datetime.hour
            new_s3 = row[id_eloc]
            #
            a = row[id_sloc]
            dur, fare = eval(row[id_dur]), eval(row[id_fare])
            #
            state_action_fare_dur[(s1, s2, s3, a)][0] += fare
            state_action_fare_dur[(s1, s2, s3, a)][1] += setup_time + dur
            #
            if Qsa_value[(new_s1, new_s2, new_s3, IN_AP)] > Qsa_value[(new_s1, new_s2, new_s3, OUT_AP)] :
                future_max_q_value = Qsa_value[(new_s1, new_s2, new_s3, IN_AP)]
            else:
                future_max_q_value = Qsa_value[(new_s1, new_s2, new_s3, OUT_AP)]
            #
            alter_a = OUT_AP if a == IN_AP else IN_AP
            if state_action_fare_dur[(s1, s2, s3, alter_a)][1] == 0:
                op_cost = 0
            else:
                op_cost = (setup_time + dur) * state_action_fare_dur[(s1, s2, s3, alter_a)][0] / state_action_fare_dur[(s1, s2, s3, alter_a)][1] 
            qrs = fare - op_cost + GAMMA * future_max_q_value
            Qsa_value[(s1, s2, s3, a)] = \
                        (1 - ALPHA) * Qsa_value[(s1, s2, s3, a)] + ALPHA * qrs
            count += 1
            if count % MOD_STAN == 0:
                print '%s, %d' % (yymm, count)
                logging_msg('%s, %d' % (yymm, count))
                save_pickle_file('%s/ALPHA-%.2f-GAMMA-%.2f-q-value-fare-dur-%s.pkl' % (ALPHA_GAMMA_dir, ALPHA, GAMMA, yymm), [Qsa_value, state_action_fare_dur])
        save_pickle_file('%s/ALPHA-%.2f-GAMMA-%.2f-q-value-fare-dur-%s.pkl' % (ALPHA_GAMMA_dir, ALPHA, GAMMA, yymm), [Qsa_value, state_action_fare_dur])
    print 'end the file; %s' % yymm
    logging_msg('end the file; %s' % yymm)

if __name__ == '__main__':
    run()
