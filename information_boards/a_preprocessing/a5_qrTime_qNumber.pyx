import __init__
#
from information_boards import dpaths, prefixs
#
from taxi_common.file_handling_functions import get_all_files, check_dir_create, get_fn_only
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import csv

logger = get_logger()


if_dpath = dpaths['eeTime', 'ap']
if_prefixs = prefixs['eeTime', 'ap']
#
of_dpath = dpaths['qrTime_qNumber', 'ap']
of_prefixs = prefixs['qrTime_qNumber', 'ap']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(yymm):
    for fn in get_all_files(if_dpath, '%s%s*' % (if_prefixs, yymm)):
        fpath = '%s/%s' % (if_dpath, fn)
        process_daily(fpath)


def process_daily(fpath):
    fn = get_fn_only(fpath)
    _, _, yymmdd = fn[:-len('.csv')].split('-')
    from traceback import format_exc
    try:
        df = pd.read_csv(fpath)
        terminals = [ter for ter in set(df['pickUpTerminal']).union(set(df['prevEndTerminal'])) if ter != 'X']
        ofpath = '%s/%s%s.csv' % (of_dpath, of_prefixs, yymmdd)
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['vid', 'did',
                           'pickupTime', 'dropoffTime', 'duration', 'fare',
                           'enteringTime', 'exitingTime',
                           'pickUpTerminal',
                           'prevEndTerminal', 'prevTripEndTime',
                           'year', 'month', 'day', 'hour', 'dow',
                           'qrTime', 'productivity']
            new_headers += terminals
            new_headers += ['minTer']
            writer.writerow(new_headers)
        #
        logger.info('handle the file; %s' % fn)
        with open(fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                prevEndTerminal, pickUpTerminal = (row[hid[cn]] for cn in ['prevEndTerminal', 'pickUpTerminal'])
                pickupTime = eval(row[hid['pickupTime']])
                duration, fare = map(eval, (row[hid[cn]] for cn in ['duration', 'fare']))
                prevTripEndTime = eval(row[hid['prevTripEndTime']])
                if prevEndTerminal == pickUpTerminal:
                    qrTime = pickupTime - eval(row[hid['prevTripEndTime']])
                else:
                    if row[hid['enteringTime']] == 'inf':
                        qrTime = 0
                    else:
                        enteringTime = eval(row[hid['enteringTime']])
                        if enteringTime < pickupTime:
                            qrTime = pickupTime - enteringTime
                        else:
                            qrTime = 0
                new_row = [row[hid[cn]] for cn in ['vid', 'did',
                                                   'pickupTime', 'dropoffTime', 'duration', 'fare',
                                                   'enteringTime', 'exitingTime',
                                                   'pickUpTerminal',
                                                   'prevEndTerminal', 'prevTripEndTime',
                                                   'year', 'month', 'day', 'hour', 'dow']]
                new_row += [qrTime, fare / float(qrTime + duration)]
                minTer, minQN = None, 1e400
                for ter in terminals:
                    ter_df = df[(df['pickUpTerminal'] == ter)]
                    num_entered = len(ter_df[(ter_df['enteringTime'] <= prevTripEndTime)])
                    num_exited = len(ter_df[(ter_df['exitingTime'] <= prevTripEndTime)])
                    QN = num_entered - num_exited
                    new_row += [QN]
                    if ter != 'BudgetT' and QN < minQN:
                        minTer = ter
                        minQN = QN
                new_row += [minTer]
                with open(ofpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], yymmdd), 'w') as f:
            f.write(format_exc())
        raise


if __name__ == '__main__':
    run('0901')
