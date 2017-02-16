import __init__
'''
'''
from community_analysis import dpaths, prefixs
from community_analysis import groupEvolution_fpath
#
from taxi_common import ss_drivers_dpath, ss_drivers_prefix
from taxi_common.file_handling_functions import load_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
#
import csv

logger = get_logger()


def run():
    yearDriver_gn = {}
    whole_ss_drivers = set()
    tm = 'spendingTime'
    for year in ['2009', '2010', '2011', '2012']:
        gp_dpath = dpaths[tm, year, 'groupPartition']
        gp_prefix = prefixs[tm, year, 'groupPartition']
        gp_drivers_fpath = '%s/%sdrivers.pkl' % (gp_dpath, gp_prefix)
        gp_drivers = load_pickle_file(gp_drivers_fpath)
        for gn, drivers in gp_drivers.iteritems():
            for did in drivers:
                yearDriver_gn[year, did] = gn
        yy = year[2:]
        for fn in get_all_files(ss_drivers_dpath, '%s%s*.pkl' % (ss_drivers_prefix, yy)):
            ss_drivers_fpath = '%s/%s' % (ss_drivers_dpath, fn)
            ss_drivers = load_pickle_file(ss_drivers_fpath)
            for did in ss_drivers:
                whole_ss_drivers.add(did)
    with open(groupEvolution_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = ['did', 'G2009', 'G2010', 'G2011', 'G2012']
        writer.writerow(header)
        for did in whole_ss_drivers:
            new_row = [did]
            for year in ['2009', '2010', '2011', '2012']:
                k = (year, did)
                if yearDriver_gn.has_key(k):
                    gn = yearDriver_gn[k]
                else:
                    gn = 'X'
                new_row += [gn]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()
