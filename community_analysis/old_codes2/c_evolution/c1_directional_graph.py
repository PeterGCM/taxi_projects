import community_analysis.c_evolution
#
from community_analysis import ld_dir, lm_dg_dir, com_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, \
                                                save_pickle_file, remove_create_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv
import networkx as nx


def run():
    remove_create_dir(lm_dg_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for mm in range(1, 12):
        yymm = '09%02d' % mm
        # process_files(yymm)
        put_task(process_files, [yymm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
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

    nodes = set()
    for _, cn in top_five_com:
        for nid in nx.read_gpickle('%s/%s-%s.pkl' % (target_dpath, yyyy, cn)).nodes():
            nodes.add(nid)
    ld_yymm_dir = ld_dir + '/%s' % yymm
    #
    num_days = 0
    pairs_day_counting = {}
    for fn in get_all_files(ld_yymm_dir, '', '.pkl'):
        daily_pairs = set()
        num_days += 1
        print 'read', fn
        daily_linkage = load_pickle_file('%s/%s' % (ld_yymm_dir, fn))
        while daily_linkage:
            _did0, _did0_num_pickup, _did0_linkage = daily_linkage.pop()
            did0 = int(_did0)
            if did0 not in nodes:
                continue
            for _did1, num_linkage in _did0_linkage.iteritems():
                did1 = int(_did1)
                if did1 not in nodes:
                    continue
                if (did0, did1) not in daily_pairs:
                    daily_pairs.add((did0, did1))
                    if not pairs_day_counting.has_key((did0, did1)):
                        pairs_day_counting[(did0, did1)] = 0
                    pairs_day_counting[(did0, did1)] += 1
    #
    N, lm = set(), []
    for (k0, k1), v in pairs_day_counting.iteritems():
        N.add(k0); N.add(k1)
        lm.append([(k0, k1), v])
    lm_fn = '%s-D(%d)-N(%d)-E(%d).pkl' % (yymm, num_days, len(N), len(lm))
    print 'lm saving'
    save_pickle_file('%s/%s' % (lm_dg_dir, lm_fn), lm)


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise