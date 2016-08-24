import __init__
#
from community_analysis.__init__ import pg_dir, com_log_dir, logs_dir
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
#
import csv
import networkx as nx


def run():
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
    top_five_com = sorted(com_sgth_fname,reverse=True)[:5]
    #
    cl_yyyy_dir = '%s/%s' % (com_log_dir, target); check_dir_create(cl_yyyy_dir)
    com_log_fn = '%s/%s-log-community.csv' % (cl_yyyy_dir, target)
    with open(com_log_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['time', 'i', 'j', 'did', 'community'])
    nid_cn = {}
    for _, fn in top_five_com:
        _, com_name = fn[:-len('.pkl')].split('-')
        #
        for nid in nx.read_gpickle('%s/%s/%s' % (pg_dir, target, fn)).nodes():
            nid_cn[nid] = com_name
    print 'Finish selecting top five communities'
    for m in range(1, 12):
        yymm_dir = '%s/09%02d' % (logs_dir, m)
        for day in sorted([int(fn[:-len('.csv')]) for fn in get_all_files(yymm_dir, '', '.csv')]):
            fn = '%d.csv' % day
            print 'Start handling', fn
            with open('%s/%s' % (yymm_dir, fn), 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    did = eval(row[hid['did']])
                    if not nid_cn.has_key(did):
                        continue
                    with open(com_log_fn, 'a') as w_csvfile:
                        writer = csv.writer(w_csvfile)
                        writer.writerow([row[hid['time']], row[hid['i']], row[hid['j']], did, nid_cn[did]])
            print 'End handling', fn

if __name__ == '__main__':
    run()