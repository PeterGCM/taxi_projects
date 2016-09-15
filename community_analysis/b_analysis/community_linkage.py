import community_analysis.c_evolution
#
from community_analysis.__init__ import pg_dir, com_linkage_dir, ld_dir
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, load_pickle_file, save_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import networkx as nx


def run():
    init_multiprocessor(11)
    count_num_jobs = 0
    for mm in range(1, 12):
        put_task(process_files, ['09%02d' % mm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
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
    com_nid = set()
    for _, fn in top_five_com:
        _, com_name = fn[:-len('.pkl')].split('-')
        #
        for nid in nx.read_gpickle('%s/%s/%s' % (pg_dir, target, fn)).nodes():
            com_nid.add(nid)
    cl_yyyy_dir = '%s/%s' % (com_linkage_dir, target); check_dir_create(cl_yyyy_dir)

    yymm_dir = '%s/%s' % (ld_dir, yymm)
    mon_di_linkage = {}
    for day in sorted([int(fn[:-len('.pkl')]) for fn in get_all_files(yymm_dir, '', '.pkl')]):
        fn = '%d.pkl' % day
        print 'Start handling', fn
        daily_linkage = load_pickle_file('%s/%s' % (yymm_dir, fn))
        while daily_linkage:
            _did0, _did0_num_pickup, _did0_linkage = daily_linkage.pop()
            did0 = int(_did0)
            if did0 not in com_nid:
                continue
            for _did1, num_linkage in _did0_linkage.iteritems():
                did1 = int(_did1)
                if did1 not in com_nid:
                    continue
                k = (did0, did1)
                if not mon_di_linkage.has_key(k):
                    mon_di_linkage[k] = 0
                mon_di_linkage[k] += num_linkage
    com_linkage_fn = '%s/%s-linkage-community.pkl' % (cl_yyyy_dir, yymm)
    save_pickle_file(com_linkage_fn, mon_di_linkage)


if __name__ == '__main__':
    run()