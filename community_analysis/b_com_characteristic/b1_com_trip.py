import __init__
#
from __init__ import whole_trip_prefix, com_trip_prefix
from community_analysis.__init__ import pg_dir, trip_dir, com_trip_dir
#
from taxi_common.file_handling_functions import get_all_files, check_dir_create
#
import networkx as nx
import csv


def run():
    yyyy = 2009
    target = '%d' % yyyy
    target_dir = '%s/%s' % (pg_dir, target)
    com, nid_com = {}, {}
    for fn in get_all_files(target_dir, '2009-', '.pkl'):
        if fn.endswith('whole.pkl'):
            continue
        print fn
        _, cnum_str = fn[:-len('.pkl')].split('-')
        cnum = eval(cnum_str[len('COM('):-len(')')])
        print fn, cnum
        nxG = nx.read_gpickle('%s/%s' % (target_dir, fn))
        com[cnum] = []
        for n in nxG.nodes():
            com[cnum].append(n)
            nid_com[n] = cnum
    #

    target = '2009'
    target_dir = '%s/%s' % (pg_dir, target)
    #
    summary_fn = '%s/%s_summary.csv' % (target_dir, target)
    com_sgth_fname = []
    with open(summary_fn, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            com_sgth_fname.append([eval(row[hid['tie-strength']]), row[hid['fname']]])
    top_five_com = sorted(com_sgth_fname, reverse=True)[:5]
    nid_cn = {}
    for _, fn in top_five_com:
        _, com_name = fn[:-len('.pkl')].split('-')
        #
        for nid in nx.read_gpickle('%s/%s/%s' % (pg_dir, target, fn)).nodes():
            nid_cn[nid] = com_name

    ct_yyyy_dir = '%s/%s' % (com_trip_dir, target); check_dir_create(ct_yyyy_dir)
    ctrip_fn = '%s/%s-trip-community.csv' % (ct_yyyy_dir, target)
    with open(ctrip_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['time', 'yy', 'mm', 'did', 'cnum', 'si', 'sj', 'ei', 'ej', 'distance', 'duration', 'fare'])
    for m in range(1, 12):
        yymm = target[-2:] + '%02d' % m
        print yymm
        yymm_dir = '%s/%s' % (trip_dir, yymm)
        for fn in get_all_files(yymm_dir, '', '.csv'):
            with open('%s/%s' % (yymm_dir, fn), 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    did = eval(row[hid['did']])
                    if not nid_cn.has_key(did):
                        continue
                    if not nid_com.has_key(did):
                        continue
                    k = nid_com[did]
                    with open(ctrip_fn, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        new_row = [
                            row[hid['time']], yymm[:2], yymm[-2:],
                            row[hid['did']], k,
                            row[hid['si']], row[hid['sj']],
                            row[hid['ei']], row[hid['ej']],
                            row[hid['distance']], row[hid['duration']], row[hid['fare']]
                        ]
                        writer.writerow(new_row)


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise