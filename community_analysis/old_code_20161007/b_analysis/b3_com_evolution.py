import __init__
#
from community_analysis import top5_com_dir, cevol_dir, clink_dir
#
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file, get_all_files
#
import networkx as nx
import csv

def run():
    check_dir_create(cevol_dir)
    #
    fn = '2009-CD(184)-thD(82).pkl'
    yyyy, str_CD, str_thD = fn[:-len('.pkl')].split('-')
    CD = int(str_CD[len('CD('):-len(')')])
    thD = int(str_thD[len('thD('):-len(')')])
    top5_com_drivers = load_pickle_file('%s/%s' % (top5_com_dir, fn))
    clink_thD_dpath = '%s/%s-CD(%d)-thD(%d)' % (clink_dir, yyyy, CD, thD)
    cevol_thD_dpath = '%s/%s-CD(%d)-thD(%d)' % (cevol_dir, yyyy, CD, thD)
    check_dir_create(cevol_thD_dpath)
    for cn in top5_com_drivers.iterkeys():
        evol_summary_fpath = '%s/%s-CD(%d)-thD(%d)-%s-evolution.csv' % (cevol_thD_dpath, yyyy, CD, thD, cn)
        with open(evol_summary_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['duration', 'num-days', 'cn',
                             'whole-driver-num', 'com-driver-num', 'out-driver-num', 'com-driver-num-ratio',
                             'whole-link-num', 'com-link-num', 'out-link-num', 'com-link-num-ratio',
                             'whole-link-weight (# of encounter days)', 'com-link-weight', 'out-link-weight', 'com-link-weight-ratio',
                             'node-order'])

    for x in range(1, 10):
        agg_m3_linkage = {}
        num_days = 0
        print '09%02d-09%02d' % (x, x + 2)
        for i in range(x, x + 3):
            target_fn = None
            for fn in get_all_files(clink_thD_dpath, '', '.pkl'):
                if fn.startswith('09%02d' % i):
                    target_fn = fn
                    break
            _, D_str, _ = target_fn[:-len('.pkl')].split('-')
            num_days += int(D_str[len('CD('):-len(')')])
            month_link = load_pickle_file('%s/%s' % (clink_thD_dpath, target_fn))
            for k, v in month_link.iteritems():
                if not agg_m3_linkage.has_key(k):
                    agg_m3_linkage[k] = 0
                agg_m3_linkage[k] += v
        #
        for cn, drivers in top5_com_drivers.iteritems():
            m3_wd, m3_cd = set(), set()
            m3_wl, m3_cl = {}, {}
            for (did0, did1), v in agg_m3_linkage.iteritems():
                if (did0 not in drivers) and (did1 not in drivers):
                    continue
                m3_wd.add(did0); m3_wd.add(did1)
                m3_wl[(did0, did1)] = v
                if (did0 in drivers):
                    m3_cd.add(did0)
                if (did1 in drivers):
                    m3_cd.add(did1)
                if (did0 in drivers) and (did1 in drivers):
                    m3_cl[(did0, did1)] = v
            #
            evol_summary_fpath = '%s/%s-CD(%d)-thD(%d)-%s-evolution.csv' % (cevol_thD_dpath, yyyy, CD, thD, cn)
            m3_nxG = nx.DiGraph()
            for (k0, k1), v in m3_wl.iteritems():
                m3_nxG.add_edge(k0, k1, weight=v)
            node_order_by_centrality, _ = zip(*sorted(nx.degree_centrality(m3_nxG).items(), key=lambda x: x[-1], reverse=True))
            wlw, clw = sum(m3_wl.values()), sum(m3_cl.values())
            with open(evol_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = ['09%02d-09%02d' % (x, x + 2), num_days, cn,
                           len(m3_wd), len(m3_cd), len(m3_wd) - len(m3_cd), len(m3_cd) / float(len(m3_wd)),
                           len(m3_wl), len(m3_cl), len(m3_wl) - len(m3_cl), len(m3_cl) / float(len(m3_wl)),
                           wlw, clw, wlw - clw, clw / float(wlw),
                           str(node_order_by_centrality)]
                writer.writerow(new_row)

    for cn, drivers in top5_com_drivers.iteritems():
        evol_summary_fpath = '%s/%s-CD(%d)-thD(%d)-%s-evolution.csv' % (cevol_thD_dpath, yyyy, CD, thD, cn)
        core_members_by_evol = None
        with open(evol_summary_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                if not core_members_by_evol:
                    core_members_by_evol = set(eval(row[hid['node-order']]))
                else:
                    cur_members = set(eval(row[hid['node-order']]))
                    core_members_by_evol.intersection_update(cur_members)
        #
        with open(evol_summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = ['original community members (%d): %s' % (len(drivers), tuple(drivers))]
            writer.writerow(new_row)
            new_row = ['core members by evolution (%d): %s' % (len(core_members_by_evol), tuple(core_members_by_evol))]
            writer.writerow(new_row)
            diff_mem = core_members_by_evol.difference(set(drivers))
            new_row = ['core members - original community (%d): %s' % (len(diff_mem), tuple(diff_mem))]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()