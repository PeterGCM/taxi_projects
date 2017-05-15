import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO, MIN_RATIO_RESIDUAL
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file, load_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
import statsmodels.api as sm
from traceback import format_exc
import csv

logger = get_logger()
numWorker = 11
#
year = '20%02d' % 9
depVar = 'roamingTime'
# depVar = 'interTravelTime'
#
#
if_dpath = dpaths[depVar, 'priorPresence']
if_prefix = prefixs[depVar, 'priorPresence']

of_dpath = dpaths[depVar, 'individual']
of_prefix = prefixs[depVar, 'individual']


try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(processorNum):
    for i, fn in enumerate(get_all_files(if_dpath, '%s%s*.csv' % (if_prefix, year))):
        if i % numWorker != processorNum:
            continue
        fpath = '%s/%s' % (if_dpath, fn)
        process_file(fpath)


def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    _, _, _, _did1 = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        ofpath = '%s/%s%s-%s.csv' % (of_dpath, of_prefix, year, _did1)
        sig_fpath = '%s/%ssigRelation-%s-%s.pkl' % (of_dpath, of_prefix, year, _did1)
        if check_path_exist(ofpath):
            return None
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['did',
                      'numObservations', 'numPrevDrivers',
                      'numSigRelationship',
                      'sigPosRelation', 'sigNegRelation']
            writer.writerow(header)
        #
        logger.info('Start loading; %s-%s' % (year, _did1))
        df = pd.read_csv(fpath)
        numObservations = len(df)
        did1_df = df.drop(['month', 'day', 'hour', 'zi', 'zj', 'did'], axis=1)
        if _did1 in did1_df.columns:
            did1_df = did1_df.drop([_did1], axis=1)
        prevDrivers = [cn for cn in did1_df.columns if cn != depVar]
        numPrevDrivers = len(prevDrivers)
        #
        sigRelatioin = {k: [] for k in ['pos', 'neg']}
        for _did0 in prevDrivers:
            y = did1_df[depVar]
            X = did1_df[[_did0]]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            pv = res.pvalues[_did0]
            coef = res.params[_did0]
            if pv < SIGINIFICANCE_LEVEL:
                if coef < 0:
                    sigRelatioin['neg'] += [_did0]
                elif coef > 0:
                    sigRelatioin['pos'] += [_did0]
        with open(ofpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [_did1,
                       numObservations, numPrevDrivers,
                       len(sigRelatioin['pos']) + len(sigRelatioin['neg']),
                       '&'.join(sigRelatioin['pos']), '&'.join(sigRelatioin['neg'])]
            writer.writerow(new_row)
        save_pickle_file(sig_fpath, sigRelatioin)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s-%s' % (year, _did1)), 'w') as f:
            f.write(format_exc())
        raise


def summary_count():
    summary_fpath = '%s/%scount-%s.csv' % (of_dpath, of_prefix, year)
    with open(summary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['did',
                  'pos', 'neg']
        writer.writerow(header)
    for fn in get_all_files(of_dpath, '%scount-%s-*.pkl' % (of_prefix, year)):
        _, _, _, _, _did1 = fn[:-len('.csv')].split('-')
        countRelation = load_pickle_file('%s/%s' % (of_dpath, fn))
        with open(summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = [int(_did1),
                      countRelation['pos'], countRelation['neg']]
            writer.writerow(new_row)


if __name__ == '__main__':
    summary_count()
