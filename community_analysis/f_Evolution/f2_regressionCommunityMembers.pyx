import __init__
#
'''

'''
#
from community_analysis import tfZ_TP_dpath, tfZ_TP_prefix
from community_analysis import dpaths, prefixs
from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO, MIN_RATIO_RESIDUAL
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import csv
import pandas as pd
import statsmodels.api as sm
from traceback import format_exc

logger = get_logger()


def run(processorNum):
    ir = 'groupEvolution'
    #
    tm = 'spendingTime'
    year = '2009'
    check_dir_create(dpaths[tm, year, ir])
    #
    ir = 'groupTrips'
    for i, fn in enumerate(get_all_files(dpaths[tm, year, ir], '%s*.csv' % (prefixs[tm, year, ir]))):
        if len(fn[:-len('.csv')].split('-')) == 5:
            continue
        _, _, _, gn = fn[:-len('.csv')].split('-')
        if gn == 'X':
            continue
        if i % 7 != processorNum:
            continue
        process_file('%s/%s' % (dpaths[tm, year, ir], fn))


def process_file(fpath):
    fn = get_fn_only(fpath)
    logger.info('Start handling; %s' % fn)
    _, _, _, gn = fn[:-len('.csv')].split('-')
    try:
        tm = 'spendingTime'
        year = '2009'
        ge_dpath = dpaths[tm, year, 'groupEvolution']
        ge_prefix = prefixs[tm, year, 'groupEvolution']
        ge_fpath = '%s/%s%s.csv' % (ge_dpath, ge_prefix, gn)
        with open(ge_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            header = ['groupName',
                      'did0', 'did1',
                      'pv', 'coef']
            writer.writerow(header)
        #
        logger.info('Start loading; %s' % (fn))
        df = pd.read_csv(fpath)
        num_drivers = len(set(df['did']))
        tm = 'roamingTime'
        for i, did1 in enumerate(set(df['did'])):
            if i % 10 == 0:
                logger.info('Doing regression %.2f; %s' % (i / float(num_drivers), fn))
            did1_df = df[(df['did'] == did1)].copy(deep=True)
            did1_df = did1_df.drop(['time','year','month','day','hour',
                                    'did','groupName','zi','zj','zizj','priorPresence',
                                    'start-long','start-lat','distance','duration','fare'], axis=1)
            if '%d' % did1 in did1_df.columns:
                did1_df = did1_df.drop(['%d' % did1], axis=1)
            #
            candi_dummies = []
            for i, vs in enumerate(zip(*did1_df.values)):
                if did1_df.columns[i] == tm:
                    continue
                candi_dummies.append(did1_df.columns[i])
            y = did1_df[tm]
            X = did1_df[candi_dummies]
            X = sm.add_constant(X)
            SP_res = sm.OLS(y, X, missing='drop').fit()
            for _did0, pv in SP_res.pvalues.iteritems():
                if _did0 == 'const':
                    continue
                coef = SP_res.params[_did0]
                with open(ge_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_row = [gn,
                              int(_did0), did1,
                              pv, coef]
                    writer.writerow(new_row)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s' % (fn)), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run(0)
