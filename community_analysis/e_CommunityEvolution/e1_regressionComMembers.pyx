import __init__
#
'''

'''
#
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only
from taxi_common.log_handling_functions import get_logger
#
import csv
import pandas as pd
import numpy as np
import statsmodels.api as sm
from traceback import format_exc

logger = get_logger()
numWorkers = 7
#
year = '20%02d' % 9
depVar = 'roamingTime'
# depVar = 'interTravelTime'
#
if_dpath = dpaths[depVar, 'comTrips']
if_prefixs = prefixs[depVar, 'comTrips']
of_dpath = dpaths[depVar, 'comEvolution']
of_prefixs = prefixs[depVar, 'comEvolution']
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(processorNum):
    for i, fn in enumerate(get_all_files(if_dpath, '%s*.csv' % (if_prefixs))):
        if i % numWorkers != processorNum:
            continue
        process_file('%s/%s' % (if_dpath, fn))


def process_file(fpath):
    fn = get_fn_only(fpath)
    logger.info('Start handling; %s' % fn)
    _, _, _, cn = fn[:-len('.csv')].split('-')
    try:
        ce_fpath = '%s/%s%s-%s.csv' % (of_dpath, of_prefixs, year, cn)
        with open(ce_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['groupName',
                      'did0', 'did1',
                      'pv', 'coef']
            writer.writerow(header)
        #
        logger.info('Start loading; %s' % (fn))
        df = pd.read_csv(fpath)
        num_drivers = len(set(df['did']))
        for i, did1 in enumerate(set(df['did'])):
            if i % 10 == 0:
                logger.info('Doing regression %.2f; %s' % (i / float(num_drivers), fn))
            did1_df = df[(df['did'] == did1)].copy(deep=True)
            hours = set(did1_df['hour'])
            dummiesH = []
            for h in hours:
                hour_str = 'H%02d' % h
                did1_df[hour_str] = np.where(did1_df['hour'] == h, 1, 0)
                dummiesH.append(hour_str)
            did1_df = did1_df.drop(['hour'], axis=1)
            ZIZJs = set(did1_df['zizj'])
            dummiesZIZJ = []
            for zizj in ZIZJs:
                did1_df[zizj] = np.where(did1_df['zizj'] == zizj, 1, 0)
                dummiesZIZJ.append(zizj)
            did1_df = did1_df.drop(['zizj'], axis=1)
            did1_df = did1_df.drop(['time','year','month','day',
                                    'did','groupName','zi','zj',
                                    'priorPresence',
                                    'start-long','start-lat','distance','duration','fare'], axis=1)
            if '%d' % did1 in did1_df.columns:
                did1_df = did1_df.drop(['%d' % did1], axis=1)
            #
            dummiesD = []
            for cn in did1_df.columns:
                if cn == depVar:
                    continue
                if cn in dummiesH:
                    continue
                if cn in dummiesZIZJ:
                    continue
                dummiesD.append(cn)
            #
            if len(did1_df) < len(dummiesD) + len(dummiesH[:-1]) + len(dummiesZIZJ[:-1]) + 1:
                continue
            y = did1_df[depVar]
            X = did1_df[dummiesD + dummiesH[:-1] + dummiesZIZJ[:-1]]
            X = sm.add_constant(X)
            try:
                res = sm.OLS(y, X, missing='drop').fit()
                for _did0, pv in res.pvalues.iteritems():
                    if _did0 == 'const':
                        continue
                    if _did0 in dummiesH:
                        continue
                    if _did0 in dummiesZIZJ:
                        continue
                    coef = res.params[_did0]
                    with open(ce_fpath, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile, lineterminator='\n')
                        new_row = [cn,
                                   int(_did0), did1,
                                   pv, coef]
                        writer.writerow(new_row)
            except np.linalg.linalg.LinAlgError:
                continue

    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s' % (fn)), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run(0)
