import __init__
#
from __init__ import whole_trip_prefix, group_trip_prefix
from community_analysis.__init__ import pg_dir, trips_dir, gtrips_dir
#
from taxi_common.file_handling_functions import get_all_files, check_dir_create
#
import networkx as nx
import csv


def run():
    yyyy = 2009
    target = '%d-TH(23)' % yyyy
    target_dir = '%s/%s' % (pg_dir, target)
    group, nid_group = {}, {}
    for fn in get_all_files(target_dir, '', '.pkl'):
        if fn.endswith('whole.pkl'):
            continue
        _, _, PD = fn[:-len('.pkl')].split('-')
        PD_num = eval(PD[len('PD('):-len(')')])
        print fn, PD_num
        nxG = nx.read_gpickle('%s/%s' % (target_dir, fn))
        group[PD_num] = []
        for n in nxG.nodes():
            group[PD_num].append(n)
            nid_group[n] = PD_num

    #
    yyyy_dir = '%s/%d' % (trips_dir, yyyy)
    for fn in get_all_files(yyyy_dir, '', '.csv'):
        _, yymm = fn[:-len('.csv')].split('-')
        missing_counter = 0
        for k in group.iterkeys():
            check_dir_create('%s/%s/%s' % (gtrips_dir, target, yymm))
            fn = '%s/%s/%s/%sG(%d).csv' % (gtrips_dir, target, yymm, group_trip_prefix, k)
            with open(fn, 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                new_headers = ['did',
                               'start-time', 'end-time',
                               'start-long', 'start-lat',
                               'end-long', 'end-lat',
                               'duration', 'fare']
                writer.writerow(new_headers)
        with open('%s/%s' % (yyyy_dir, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did = eval(row[hid['did']])
                if not nid_group.has_key(did):
                    missing_counter += 1
                    continue
                k = nid_group[did]
                gtrip_fn = '%s/%s/%s/%sG(%d).csv' % (gtrips_dir, target, yymm, group_trip_prefix, k)
                with open(gtrip_fn, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile)
                    writer.writerow(row)
        print missing_counter


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise