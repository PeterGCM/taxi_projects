import __init__
#
'''

'''
from community_analysis import tfZ_TP_dpath, tfZ_TP_prefix
from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO
from community_analysis import dpaths, prefixs
#
import pandas as pd
import numpy as np
import statsmodels.api as sm

from community_analysis import SIGINIFICANCE_LEVEL, MIN_PICKUP_RATIO
def regression(dv, df):
    oc_dv = 'roamingTime' if dv == 'spendingTime' else 'spendingTime'
    rdf = df.copy(deep=True).drop([oc_dv], axis=1)
    rdf = rdf[~(np.abs(rdf[dv] - rdf[dv].mean()) > (3 * rdf[dv].std()))]
    candi_dummies = []
    num_iter = 1
    while True:
        for i, vs in enumerate(zip(*rdf.values)):
            if rdf.columns[i] == dv:
                continue
            if sum(vs) > len(rdf) * MIN_PICKUP_RATIO * num_iter:
                candi_dummies.append(rdf.columns[i])
        if len(rdf) <= len(candi_dummies):
            candi_dummies = []
            num_iter += 1
        else:
            break
    y = rdf[dv]
    X = rdf[candi_dummies]
    X = sm.add_constant(X)
    return sm.OLS(y, X, missing='drop').fit()

reducerID = 2265 % 60
fpath = '%s/%s%s-%d.csv'% (tfZ_TP_dpath, tfZ_TP_prefix,'2012', reducerID)
df = pd.read_csv(fpath)

SP_graph = {}


for i, did1 in enumerate(set(df['did'])):
    did1_df = df[(df['did'] == did1)].copy(deep=True)
    did1_df = did1_df.drop(['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did'], axis=1)
    if '%d' % did1 in did1_df.columns:
        did1_df = did1_df.drop(['%d' % did1], axis=1)
    #
    SP_res = regression('spendingTime', did1_df)
    if SP_res.f_pvalue < SIGINIFICANCE_LEVEL:
        significant_drivers = set()
        for _did0, pv in SP_res.pvalues.iteritems():
            if _did0 == 'const':
                continue
            if pv < SIGINIFICANCE_LEVEL:
                significant_drivers.add(_did0)
        positive_ef_drivers = set()
        for _did0, cof in SP_res.params.iteritems():
            if _did0 == 'const':
                continue
            if cof > 0:
                positive_ef_drivers.add(_did0)
        for _did0 in significant_drivers.difference(positive_ef_drivers):
            print (int(_did0), did1), SP_res.params[_did0]
            SP_graph[int(_did0), did1] = SP_res.params[_did0]

print SP_graph