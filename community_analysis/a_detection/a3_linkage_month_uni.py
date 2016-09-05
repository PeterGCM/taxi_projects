import __init__
#
from community_analysis import ld_dir, lm_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, \
                                                save_pickle_file, remove_create_dir
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor


def run():
    remove_create_dir(lm_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for mm in range(1, 12):
        put_task(process_files, ['09%02d' % mm])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_files(yymm):
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
            for _did1, num_linkage in _did0_linkage.iteritems():
                did0, did1 = int(_did0), int(_did1)
                if did0 > did1:
                    did0, did1 = int(_did1), int(_did0)
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
    save_pickle_file('%s/%s' % (lm_dir, lm_fn), lm)

if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise