import __init__
#
from community_analysis import lm_dg_dir, cevol_dir
#
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create
#
import csv



def run():



    check_dir_create(cevol_dir)
    evol_summary_fpath = '%s/2009-community-evolution.csv' % (cevol_dir)
    with open(evol_summary_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['duration', 'num-days', 'cname', 'node-num', 'edge-num', 'edge-weight-sum', 'tie-strengh', 'node-order'])

    for x in range(1, 10):
        agg_m3_linkage = {}
        min_v, max_v = 1e400, -1e400
        for i in range(x, x + 3):
            com_linkage_fn = '%s/09%02d-linkage-community.pkl' % (lm_dg_dir, i)
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
            node_order_by_centrality, _ = zip(
                *sorted(nx.degree_centrality(sub_g).items(), key=lambda x: x[-1], reverse=True))

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