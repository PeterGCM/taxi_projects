import __init__
#
from community_analysis import ft_trips_dir, ft_trips_prefix
from community_analysis import dw_graph_dir, dw_graph_prefix
from community_analysis import dw_summary_fpath
#
from taxi_common.file_handling_functions import load_pickle_file
from taxi_common.charts import one_histogram
#
import numpy as np
import scipy.stats.stats as st
import csv
#
NUM_BINS = 40


def run():
    with open(dw_summary_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['year', 'days','numDrivers',
                         'numPickupsTotal', 'numPickupsAverage', 'numPickupsSD',
                            'numPickupsMin', 'numPickupsMax', 'numPickupsSkew',
                         'weightTotal', 'weightAverage', 'weightSD',
                            'weightMin', 'weightMax', 'weightSkew'])
    for y in range(9, 13):
        yyyy = '20%02d' % y
        print 'Handle %s' % yyyy
        year_dw_graph_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_prefix, yyyy)
        year_dw_graph = load_pickle_file(year_dw_graph_fpath)
        num_drivers = 0
        pickups, weights = [], []
        for did, num_pickup, weighted_link in year_dw_graph:
            num_drivers += 1
            pickups.append(num_pickup)
            weights += weighted_link.values()
        pickups_np, weights_np = np.asarray(pickups), np.asarray(weights)
        month_day = set()
        for m in range(1, 12):
            yymm = '%02d%02d' % (y, m)
            ft_trips_fpath = '%s/%s%s.csv' % (ft_trips_dir, ft_trips_prefix, yymm)
            with open(ft_trips_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    day = row[hid['day']]
                    month_day.add((m, day))
        with open(dw_summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([yyyy, len(month_day), num_drivers,
                             pickups_np.sum(), pickups_np.mean(), pickups_np.std(),
                                pickups_np.min(), pickups_np.max(), st.skew(pickups_np),
                             weights_np.sum(), weights_np.mean(), weights_np.std(),
                             weights_np.min(), pickups_np.max(), st.skew(weights_np)])
        #
        one_histogram((6, 6), '', '# of pickups', 'Probability', NUM_BINS,
                        pickups_np, '%s/num-pickups-%s' % (dw_graph_dir, yyyy))
        one_histogram((6, 6), '', 'weights', 'Probability', NUM_BINS,
                      weights_np, '%s/weights-%s' % (dw_graph_dir, yyyy))


if __name__ == '__main__':
    run()