import __init__
#
from community_analysis.__init__ import lm_dir, la_dir
#
from taxi_common.file_handling_functions import load_pickle_file, get_all_files, check_dir_create, save_pickle_file


def run():
    yyyy = '2009'
    lm_yyyy_dir = lm_dir + '/%s' % yyyy
    day_counting, max_num_days = 0, -1e400
    pairs_day_counting = {}
    N = set()
    for fn in get_all_files(lm_yyyy_dir, '', '.pkl'):
        lm = load_pickle_file('%s/%s' % (lm_yyyy_dir, fn))
        _, D, _, _, _ = lm[:-len('.pkl')].split('-')
        day_counting += int(D)
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