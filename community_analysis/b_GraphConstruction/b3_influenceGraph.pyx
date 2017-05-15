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
if_dpath1 = dpaths[depVar, 'priorPresence']
if_prefix1 = prefixs[depVar, 'priorPresence']
if_dpath2 = dpaths[depVar, 'sigRelation']
if_prefix2 = prefixs[depVar, 'sigRelation']

of_dpath = dpaths[depVar, 'influenceGraph']
of_prefix = prefixs[depVar, 'influenceGraph']


try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(processorNum):
    for i, fn in enumerate(get_all_files(if_dpath1, '%s%s*.csv' % (if_prefix1, year))):
        if i % numWorker != processorNum:
            continue
        fpath = '%s/%s' % (if_dpath1, fn)
        process_file(fpath)


def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    _, _, _, _did1 = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        ig_fpath = '%s/%s%s-%s.pkl' % (of_dpath, of_prefix, year, _did1)
        count_fpath = '%s/%scount-%s-%s.pkl' % (of_dpath, of_prefix, year, _did1)
        if check_path_exist(ig_fpath):
            return None
        #
        logger.info('Start loading; %s-%s' % (year, _did1))
        sr_fpath = '%s/%s%s-%s.csv' % (if_dpath2, if_prefix2, year, _did1)
        inDepVar = []
        with open(sr_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            header = reader.next()
            hid = {h: i for i, h in enumerate(header)}
            for row in reader:
                sigRelation = row[hid['sigRelation']]
                if len(sigRelation) == 0:
                    continue
                for _did0 in sigRelation.split('&'):
                    inDepVar += [_did0]
        if not inDepVar:
            return None
        df = pd.read_csv(fpath)
        influenceGraph = {}
        countRelation = {k: 0 for k in ['pos', 'neg']}
        for _did0 in inDepVar:
            y = df[depVar]
            X = df[[_did0]]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            coef = res.params[_did0]
            if coef < 0:
                countRelation['neg'] += 1
                influenceGraph[int(_did0), int(_did1)] = (res.pvalues[_did0], coef)
            elif coef > 0:
                countRelation['pos'] += 1
        #
        logger.info('Start pickling; %s-%s' % (year, _did1))
        save_pickle_file(ig_fpath, influenceGraph)
        save_pickle_file(count_fpath, countRelation)
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
