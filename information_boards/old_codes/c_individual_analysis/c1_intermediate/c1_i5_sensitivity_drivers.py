#
'''

'''
#
import csv
import datetime

import numpy as np
import pandas as pd
import statsmodels.api as sm
from information_boards.b_aggregated_analysis import ap_ep_dir, ap_ep_prefix

from information_boards import DIn_PIn, SEC60
from information_boards.old_codes.c_individual_analysis import ssd_apIn_fpath, ssd_sensitivity_fpath
from taxi_common import full_time_driver_dir, ft_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist
from taxi_common.log_handling_functions import get_logger

logger = get_logger()


def run():
    if not check_path_exist(ssd_apIn_fpath):
        with open(ssd_apIn_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            headers = ['apQTime', 'apIn', 'did']
            writer.writerow(headers)
            for m in xrange(1, 13):
                yymm = '10%02d' % m
                if yymm in ['1010']:
                    continue
                logger.info('Start handling; %s' % yymm)
                ft_drivers = map(int, load_pickle_file('%s/%s%s.pkl' % (full_time_driver_dir, ft_drivers_prefix, yymm)))
                ap_ep_fpath = '%s/%s%s.csv' % (ap_ep_dir, ap_ep_prefix, yymm)
                with open(ap_ep_fpath, 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    hid = {h: i for i, h in enumerate(headers)}
                    handling_day = 0
                    for row in reader:
                        did = int(row[hid['did']])
                        if did not in ft_drivers:
                            continue
                        t = eval(row[hid['start-time']])
                        cur_dt = datetime.datetime.fromtimestamp(t)
                        if handling_day != cur_dt.day:
                            logger.info('...ing; %s(%dth)' % (yymm, handling_day))
                            handling_day = cur_dt.day
                        apIn = 1 if int(row[hid['trip-mode']]) == DIn_PIn else 0
                        apQTime = eval(row[hid['queueing-time']]) / float(SEC60)
                        new_row = [apQTime, apIn, did]
                        writer.writerow(new_row)
    #
    df = pd.read_csv(ssd_apIn_fpath)
    df = df[~(np.abs(df['apQTime'] - df['apQTime'].mean()) > (3 * df['apQTime'].std()))]
    minNumSample = 40
    with open(ssd_sensitivity_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        headers = ['did', 'F_pValue', 'rSqure', 'rSqureAdj', 'coef_apIn', 'pValue_apIn', 'coef_const', 'pValue_const']
        writer.writerow(headers)
        for did in set(df['did']) :
            did_df = df[(df['did'] == did)]
            if len(did_df) < minNumSample:
                continue

            if len(did_df[(did_df['apIn'] == 0)]) < 4:
                continue
            y = did_df['apQTime']
            X = did_df['apIn']
            X = sm.add_constant(X)
            res = sm.OLS(y, X).fit()
            if np.isnan(res.f_pvalue):
                continue
            try:
                writer.writerow([did, res.f_pvalue, res.rsquared, res.rsquared_adj,
                                 res.params['apIn'], res.pvalues['apIn'], res.params['const'], res.pvalues['const']])
            except Exception as _:
                pass



if __name__ == '__main__':
    run()
    # from traceback import format_exc
    # #
    # try:
    #     run()
    # except Exception as _:
    #     import sys
    #     with open('___error_%s.txt' % (sys.argv[0]), 'w') as f:
    #         f.write(format_exc())
    #     raise
