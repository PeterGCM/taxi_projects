import __init__
#
from community_analysis import lm_dir, la_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, \
                                                save_pickle_file, check_dir_create


def run():
    check_dir_create(la_dir)
    #
    yyyy = '2009'
    day_counting = 0
    pairs_day_counting = {}
    N = set()
    for fn in get_all_files(lm_dir, '', '.pkl'):
        _, D, _, _ = fn[:-len('.pkl')].split('-')
        day_counting += int(D[len('D('):-len(')')])
        lm = load_pickle_file('%s/%s' % (lm_dir, fn))
        print 'load', fn
        for (k0, k1), num_days in lm:
            N.add(k0); N.add(k1)
            if (k0, k1) not in pairs_day_counting:
                pairs_day_counting[(k0, k1)] = 0
            pairs_day_counting[(k0, k1)] += num_days
    fpath = '%s/%s-CD(%d)-N(%d)-E(%d).pkl' % (
        la_dir, yyyy, day_counting, len(N), len(pairs_day_counting))
    save_pickle_file(fpath, pairs_day_counting)


    #



if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise