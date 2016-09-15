import community_analysis.c_evolution
#
from community_analysis.__init__ import pg_dir, com_linkage_dir, cevol_dir
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, load_pickle_file, save_pickle_file
#
import networkx as nx
import csv
import matplotlib.pyplot as plt


def run():
    target = '2009'
    cl_yyyy_dir = '%s/%s' % (com_linkage_dir, target)
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
    com_nid = []
    nid_git = {}
    base_G = nx.Graph()
    for i, (_, fn) in enumerate(top_five_com):
        _, com_name = fn[:-len('.pkl')].split('-')
        #
        nids = []
        for nid in nx.read_gpickle('%s/%s/%s' % (pg_dir, target, fn)).nodes():
            nids.append(nid)
            nid_git[nid] = i
            base_G.add_node(nid)
        com_nid.append((com_name, nids))
    pos = nx.circular_layout(base_G)
    num_com = i + 1

    cevol_yyyy_dir = '%s/%s' % (cevol_dir, target); check_dir_create(cevol_yyyy_dir)
    evol_summary_fpath = '%s/community-evolution.csv' %(cevol_yyyy_dir)
    with open(evol_summary_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['duration', 'cname', 'node-num', 'edge-num', 'edge-weight-sum', 'tie-strengh', 'node-order'])


    for x in range(1, 10):
        agg_m3_linkage = {}
        min_v, max_v = 1e400, -1e400
        for i in range(x, x+3):
            com_linkage_fn = '%s/09%02d-linkage-community.pkl' % (cl_yyyy_dir, i)
            month_linkage = load_pickle_file(com_linkage_fn)
            for k, v in month_linkage.iteritems():
                if not agg_m3_linkage.has_key(k):
                    agg_m3_linkage[k] = 0
                agg_m3_linkage[k] += v
                if agg_m3_linkage[k] < min_v:
                    min_v = agg_m3_linkage[k]
                if max_v < agg_m3_linkage[k]:
                    max_v = agg_m3_linkage[k]
        print min_v, max_v
        m3_G = nx.DiGraph()
        for (k0, k1), v in agg_m3_linkage.iteritems():
            if v < 20:
                continue
            m3_G.add_edge(k0, k1, weight=v)
        for i in range(num_com):
            com_name, nids = com_nid[i]

            sub_g = m3_G.subgraph(nids)
            plt.figure(figsize=(12, 6))

            nx.draw_networkx_nodes(sub_g, pos)
            nx.draw_networkx_labels(sub_g, pos)
            nx.draw_networkx_edges(sub_g, pos, alpha=0.5)
            plt.savefig('%s/%s from 09%02d to 09%02d.pdf' % (cevol_yyyy_dir, com_name, x, x + 2))
            plt.close()

            nxN = sub_g.nodes()
            _, _, weight = zip(*list(sub_g.edges_iter(data='weight', default=1)))
            num_nodes, num_edges = len(nxN), len(weight)
            node_order_by_centrality, _ = zip(*sorted(nx.degree_centrality(sub_g).items(), key=lambda x: x[-1], reverse=True))

            evol_summary_fpath = '%s/community-evolution.csv' % (cevol_yyyy_dir)
            with open(evol_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile)
                new_row = ['09%02d-09%02d' % (x, x + 2),
                           com_name, num_nodes, num_edges, sum(weight),
                           sum(weight) / float(num_nodes),
                           str(node_order_by_centrality)]
                writer.writerow(new_row)


if __name__ == '__main__':
    run()