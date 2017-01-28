import __init__
#
'''

'''
#
from community_analysis import SP_comZones_dpath, SP_comZones_prefix
from community_analysis import RP_comZones_dpath, RP_comZones_prefix
from community_analysis import SP_interesting_zone_fpath, RP_interesting_zone_fpath
from community_analysis import SIGINIFICANCE_LEVEL
#
from taxi_common.file_handling_functions import get_all_files, check_dir_create, save_pickle_file
#
import pandas as pd
import statsmodels.api as sm
import csv

sig_level = 0.10


def run():
    for dpath in [SP_comZones_dpath, RP_comZones_dpath]:
        check_dir_create(dpath)
    #
    for zone_dpath, zone_prefix in [(SP_comZones_dpath, SP_comZones_prefix),
                                    (RP_comZones_dpath, RP_comZones_prefix)]:
        for fn in get_all_files(zone_dpath, '%s*.csv' % zone_prefix):
            _, _, gn = fn[:-len('.csv')].split('-')
            reg_fpath = '%s/%s%s.pkl' % (zone_dpath, zone_prefix, gn)
            zizj_priorPresence = {}
            with open('%s/%s' % (zone_dpath, fn), 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                header = reader.next()
                hid = {h: i for i, h in enumerate(header)}
                for row in reader:
                    zizj, priorPresence = row[hid['zizj']], int(row[hid['priorPresence']])
                    if not zizj_priorPresence.has_key(zizj):
                        zizj_priorPresence[zizj] = 0
                    zizj_priorPresence[zizj] += priorPresence
            print gn, [(k, v)for k, v in zizj_priorPresence.iteritems() if v > 0]
            zizj_weight = {}
            df = pd.read_csv('%s/%s' % (zone_dpath, fn))
            for zizj, sumPriorPresence in zizj_priorPresence.iteritems():
                if sumPriorPresence < 2:
                    continue
                zizj_df = df[(df['zizj'] == zizj)]
                y = zizj_df['timeMeasure']
                X = zizj_df['priorPresence']
                X = sm.add_constant(X)
                res = sm.OLS(y, X, missing='drop').fit()
                if res.params['priorPresence'] < 0 and res.pvalues['priorPresence'] < sig_level:
                    zizj_weight[zizj] = res.params['priorPresence']

                    # write a csv file again!!
            save_pickle_file(reg_fpath, zizj_weight)


if __name__ == '__main__':
    run()
