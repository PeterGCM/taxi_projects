import __init__
#
from community_analysis.__init__ import charts_dir, la_dir
#
from taxi_common.charts import one_histogram
from taxi_common.file_handling_functions import load_pickle_file, get_all_files


def run():
    assert len(get_all_files(la_dir, '', '.pkl')) == 1
    fn = get_all_files(la_dir, '', '.pkl').pop()
    print fn
    print 'pkl file loading ...'
    pairs_day_counting = load_pickle_file('%s/%s' % (la_dir, fn))
    day_counting = pairs_day_counting.values()

    one_histogram((8, 6), '', 'The number of days in a year drivers contact', 'Probability',
                  50, day_counting, '%s/Y2009_contact_day_distribution' % charts_dir)


if __name__ == '__main__':
    run()