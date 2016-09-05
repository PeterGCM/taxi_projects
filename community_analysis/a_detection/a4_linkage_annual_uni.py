import __init__
#
from community_analysis import lm_dir, la_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, \
                                                save_pickle_file, check_dir_create, \
                                                check_path_exist


def run():
    check_dir_create(la_dir)
    #
    yyyy = '2009'
    day_counting = 0
    pairs_day_counting = {}

    print get_all_files(lm_dir, '', '.pkl')
    assert False

    for fn in get_all_files(lm_dir, '', '.pkl'):
        _, D, _, _ = fn[:-len('.pkl')].split('-')
        day_counting += int(D[len('D('):-len(')')])
        lm = load_pickle_file('%s/%s' % (lm_dir, fn))
        print 'load', fn
        for (k0, k1), num_days in lm:
            if (k0, k1) not in pairs_day_counting:
                pairs_day_counting[(k0, k1)] = 0
            pairs_day_counting[(k0, k1)] += num_days

    for ratio in [0.45, 0.5]:
        th_day = int(day_counting * ratio)
        filtered_pairs = {}
        N = set()
        for (k0, k1), num_days in pairs_day_counting.iteritems():
            if num_days < th_day:
                continue
            N.add(k0); N.add(k1)
            filtered_pairs[(k0, k1)] = num_days
        #
        fpath = '%s/%s-CD(%d)-thD(%d)-N(%d)-E(%d).pkl' % (
        la_dir, yyyy, day_counting, th_day, len(N), len(filtered_pairs))
        if check_path_exist(fpath):
            continue
        print 'Saving'
        save_pickle_file(fpath, filtered_pairs)


if __name__ == '__main__':
    from traceback import format_exc
    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise