import __init__
#
from community_analysis import com_dir, com_trip_dir, trip_dir
#
from taxi_common.file_handling_functions import get_all_files, check_dir_create, get_all_directories
#
import networkx as nx
import csv


def run():
    for dir_name in get_all_directories(com_dir):
        yyyy, str_CD, str_thD = dir_name.split('-')
        CD = int(str_CD[len('CD('):-len(')')])
        thD = int(str_thD[len('thD('):-len(')')])
        target_dpath = '%s/%s' % (com_dir, dir_name)
        print target_dpath
        summary_fpath = '%s/%s-community-summary.csv' % (target_dpath, yyyy)
        com_sgth_fname = []
        with open(summary_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            ts_header = None
            for k in hid.iterkeys():
                if k.startswith('tie-strength'):
                    ts_header = k
            assert ts_header
            for row in reader:
                com_sgth_fname.append([eval(row[hid[ts_header]]), row[hid['com-name']]])
        if len(com_sgth_fname) < 5:
            continue
        top_five_com = sorted(com_sgth_fname, reverse=True)[:5]
        nid_cn = {}
        for _, cn in top_five_com:
            for nid in nx.read_gpickle('%s/%s-%s.pkl' % (target_dpath, yyyy, cn)).nodes():
                nid_cn[nid] = int(cn[len('COM)'):-len(')')])
        #
        check_dir_create(com_trip_dir)
        ctrip_fn = '%s/%s-CD(%d)-thD(%d)-ctrip.csv' % (com_trip_dir, yyyy, CD, thD)
        with open(ctrip_fn, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['time', 'yy', 'mm', 'did', 'cnum',
                             'start-long', 'start-lat', 'end-long', 'end-lat',
                             'distance', 'duration', 'fare',
                             'si', 'sj', 'ei', 'ej'])
        #
        for m in range(1, 12):
            yymm = '%02d%02d' % (int(yyyy) - 2000, m)
            print yymm
            yymm_dir = '%s/%s' % (trip_dir, yymm)
            for fn in get_all_files(yymm_dir, '', '.csv'):
                print fn
                with open('%s/%s' % (yymm_dir, fn), 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    hid = {h: i for i, h in enumerate(headers)}
                    for row in reader:
                        did = eval(row[hid['did']])
                        if not nid_cn.has_key(did):
                            continue
                        k = nid_cn[did]
                        with open(ctrip_fn, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile)
                            new_row = [
                                row[hid['time']], yymm[:2], yymm[-2:], row[hid['did']], k,
                                row[hid['start-long']], row[hid['start-lat']], row[hid['end-long']], row[hid['end-lat']],
                                row[hid['distance']], row[hid['duration']], row[hid['fare']],
                                row[hid['si']], row[hid['sj']], row[hid['ei']], row[hid['ej']]
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