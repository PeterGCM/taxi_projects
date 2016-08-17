import __init__
#
from community_analysis.__init__ import pg_dir, com_linkage_dir, ld_dir
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, load_pickle_file, save_pkl_threading
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
    com_nid = set()
    for _, fn in top_five_com:
        _, com_name = fn[:-len('.pkl')].split('-')
        #
        for nid in nx.read_gpickle('%s/%s/%s' % (pg_dir, target, fn)).nodes():
            com_nid.add(nid)
    cl_yyyy_dir = '%s/%s' % (com_linkage_dir, target); check_dir_create(cl_yyyy_dir)
    for m in range(1, 12):
        yymm_dir = '%s/09%02d' % (ld_dir, m)
        mon_di_linkage = {}
        for day in sorted([int(fn[:-len('.pkl')]) for fn in get_all_files(yymm_dir, '', '.pkl')]):
            fn = '%d.pkl' % day
            print 'Start handling', fn
            daily_linkage = load_pickle_file('%s/%s' % (yymm_dir, fn))
            while daily_linkage:
                _did0, _did0_num_pickup, _did0_linkage = daily_linkage.pop()
                if _did0 not in com_nid:
                    continue
                for _did1, num_linkage in _did0_linkage.iteritems():
                    if _did1 not in com_nid:
                        continue
                    k = (_did0, _did1)
                    if not mon_di_linkage.has_key(k):
                        mon_di_linkage.has_key[k] = 0
                    mon_di_linkage.has_key[k] += num_linkage
        com_linkage_fn = '%s/09%02d-linkage-community.csv' % (cl_yyyy_dir, m)
        save_pkl_threading(com_linkage_fn, mon_di_linkage)

    from taxi_common.file_handling_functions import thread_writing
    if thread_writing:
        thread_writing.join()



if __name__ == '__main__':
    run()