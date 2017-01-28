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


def run():
    for dpath in [SP_comZones_dpath, RP_comZones_dpath]:
        check_dir_create(dpath)
    #
    for zone_dpath, zone_prefix, dv, interesting_zone_fpath, sig_level in [
                                    (SP_comZones_dpath, SP_comZones_prefix, 'spendingTime', SP_interesting_zone_fpath, 0.10),
                                    (RP_comZones_dpath, RP_comZones_prefix, 'roamingTime', RP_interesting_zone_fpath, 0.50)]:
        gn_interesting_zizj = {}
        for fn in get_all_files(zone_dpath, '%s*.csv' % zone_prefix):
            _, _, gn, _did0, _did1 = fn[:-len('.csv')].split('-')
            if not gn_interesting_zizj.has_key(gn):
                gn_interesting_zizj[gn] = {}
            fpath = '%s/%s' % (zone_dpath, fn)
            df = pd.read_csv(fpath)
            candi_dummies = [cn for cn in df.columns if dv != cn]
            y = df[dv]
            X = df[candi_dummies[:-1]]
            X = sm.add_constant(X)
            res = sm.OLS(y, X, missing='drop').fit()
            # if res.f_pvalue < sig_level:
            significant_zizj = set()
            for _zizj, pv in res.pvalues.iteritems():
                if _zizj == 'const':
                    continue
                if pv < sig_level:
                    significant_zizj.add(_zizj)
            positive_ef_drivers = set()
            for _zizj, cof in res.params.iteritems():
                if _zizj == 'const':
                    continue
                if cof > 0:
                    positive_ef_drivers.add(_zizj)
            for _zizj in significant_zizj.difference(positive_ef_drivers):
                zi, zj = map(int, _zizj.split('#'))
                gn_interesting_zizj[gn][zi, zj] = res.params[_zizj]
        save_pickle_file(interesting_zone_fpath, gn_interesting_zizj)


if __name__ == '__main__':
    run()
