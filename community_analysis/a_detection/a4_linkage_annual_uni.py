import __init__
#
from community_analysis import lm_dir, la_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, \
                                                save_pickle_file, remove_create_dir


def run():
    remove_create_dir(la_dir)
    #
    yyyy = '2009'
    day_counting, max_num_days = 0, -1e400
    pairs_day_counting = {}
    N = set()
    for fn in get_all_files(lm_dir, '', '.pkl'):
        _, D, _, _, _ = fn[:-len('.pkl')].split('-')
        day_counting += int(D[len('D('):-len(')')])
        lm = load_pickle_file('%s/%s' % (lm_dir, fn))
        print 'load', fn
        for (k0, k1), num_days in lm:
            N.add(k0); N.add(k1)
            if (k0, k1) not in pairs_day_counting:
                pairs_day_counting[(k0, k1)] = 0
            pairs_day_counting[(k0, k1)] += num_days
            if max_num_days < pairs_day_counting[(k0, k1)]:
                max_num_days = pairs_day_counting[(k0, k1)]
    fn = '%s-CD(%d)-MD(%d)-N(%d)-E(%d).pkl' % (yyyy, day_counting, max_num_days, len(N), len(pairs_day_counting))
    print 'Saving'
    save_pickle_file('%s/%s' % (la_dir, fn), pairs_day_counting)


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise