import community_analysis.c_evolution
#
from community_analysis import com_dir, lm_dg_dir, cevol_dir
#
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create, get_all_files
#
import csv
import networkx as nx
import matplotlib.pyplot as plt


def run():
    check_dir_create(cevol_dir)
    #
    yyyy = '2009'
    target_dpath = '%s/%s' % (com_dir, '2009-CD(184)-thD(92)')
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
    top_five_com = sorted(com_sgth_fname, reverse=True)[:5]
    cn_nodes, nid_comid = {}, {}
    base_G = nx.Graph()
    for _, cn in top_five_com:
        nodes = []
        for nid in nx.read_gpickle('%s/%s-%s.pkl' % (target_dpath, yyyy, cn)).nodes():
            nodes.append(nid)
            nid_comid[nid] = cn
            base_G.add_node(nid)
        cn_nodes[cn] = nodes
    pos = nx.circular_layout(base_G)
    #
    for cn, nodes in cn_nodes.iteritems():
        evol_summary_fpath = '%s/2009-%s-evolution.csv' % (cevol_dir, cn)
        with open(evol_summary_fpath, 'wb') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['duration', 'num-days', 'cname', 'node-num', 'edge-num', 'edge-weight-sum (# of encounter days)',
                             'avg. edge per node (edge-num / node-num)', 'avg. weight (edge-weight-sum / edge-num)',
                             'tie-strengh', 'node-order'])
    #
    for x in range(1, 10):
        agg_m3_linkage = {}
        num_days = 0
        for i in range(x, x + 3):
            target_fn = None
            for fn in get_all_files(lm_dg_dir, '', '.pkl'):
                if fn.startswith('09%02d' % i):
                    target_fn = fn
                    break
            _, D_str, _, _ = target_fn[:-len('.pkl')].split('-')
            num_days += int(D_str[len('D('):-len(')')])
            month_linkage = load_pickle_file('%s/%s' % (lm_dg_dir, target_fn))
            for k, v in month_linkage:
                if not agg_m3_linkage.has_key(k):
                    agg_m3_linkage[k] = 0
                agg_m3_linkage[k] += v
        m3_nxG = nx.DiGraph()
        for (k0, k1), v in agg_m3_linkage.iteritems():
            m3_nxG.add_edge(k0, k1, weight=v)
        #
        for cn in cn_nodes.iterkeys():
            nodes = cn_nodes[cn]
            sub_nxG = m3_nxG.subgraph(nodes)
            plt.figure(figsize=(12, 6))
            nx.draw_networkx_nodes(sub_nxG, pos)
            nx.draw_networkx_labels(sub_nxG, pos)
            nx.draw_networkx_edges(sub_nxG, pos, alpha=0.5)
            plt.savefig('%s/%s from 09%02d to 09%02d.pdf' % (cevol_dir, cn, x, x + 2))
            plt.close()

            nxN = sub_nxG.nodes()
            _, _, weight = zip(*list(sub_nxG.edges_iter(data='weight', default=1)))
            num_nodes, num_edges = len(nxN), len(weight)
            node_order_by_centrality, _ = zip(
                *sorted(nx.degree_centrality(sub_nxG).items(), key=lambda x: x[-1], reverse=True))

            evol_summary_fpath = '%s/2009-%s-evolution.csv' % (cevol_dir, cn)
            with open(evol_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                new_row = ['09%02d-09%02d' % (x, x + 2),
                           num_days, cn, num_nodes, num_edges, sum(weight),
                           num_edges / float(num_nodes), sum(weight) / float(num_edges),
                           sum(weight) / float(num_nodes), str(node_order_by_centrality)]
                writer.writerow(new_row)
    for cn in cn_nodes.iterkeys():
        evol_summary_fpath = '%s/2009-%s-evolution.csv' % (cevol_dir, cn)
        core_members = None
        with open(evol_summary_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                if not core_members:
                    core_members = set(eval(row[hid['node-order']]))
                else:
                    cur_members = set(eval(row[hid['node-order']]))
                    core_members.intersection_update(cur_members)
        #
        with open(evol_summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_row = ['core members (%d): %s' % (len(core_members), tuple(core_members))]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()