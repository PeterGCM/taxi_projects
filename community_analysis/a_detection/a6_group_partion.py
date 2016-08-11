import __init__
#
from community_analysis.__init__ import la_dir, pg_dir
#
import community
import networkx as nx

from taxi_common.file_handling_functions import load_pickle_file, get_all_files, check_dir_create

MIN_AN_DAYS = 23


def run():
    yyyy = '2009'
    print 'start',
    assert len(get_all_files(la_dir, '', '.pkl')) == 1
    fn = get_all_files(la_dir, '', '.pkl').pop()
    print fn
    print 'pkl file loading ...'
    pairs_day_counting = load_pickle_file('%s/%s' % (la_dir, fn))
    print 'finished'
    print 'Graph constructing ...'
    G = nx.Graph()
    for (k0, k1), num_days in pairs_day_counting.iteritems():
        # if num_days < MIN_AN_DAYS:
        #     continue
        G.add_edge(k0, k1, weight=num_days)

    del pairs_day_counting
    # pg_th_dir = '%s/%s-TH(%d)' % (pg_dir, yyyy, MIN_AN_DAYS); check_dir_create(pg_th_dir)
    pg_th_dir = '%s/%s' % (pg_dir, yyyy); check_dir_create(pg_th_dir)
    print 'finished'
    print 'Whole graph pickling ...'
    nx.write_gpickle(G, '%s/%s-whole.pkl' % (pg_th_dir, yyyy))
    print 'finished'
    # first compute the best partition
    print 'Partitioning ...'
    partition = community.best_partition(G)
    print 'finished'
    for i, com in enumerate(set(partition.values())):
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        print i, 'Saving sub-graph ...'
        nx.write_gpickle(G.subgraph(list_nodes), '%s/%s-COM(%d).pkl' % (pg_dir, yyyy, i))
        print 'finished'


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise