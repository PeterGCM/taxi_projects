import __init__
#
from community_analysis import ft_trips_dir, ft_trips_prefix
from community_analysis import dw_graph_dir, dw_graph_prefix
from community_analysis import dw_month3_summary_fpath
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, save_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
#
import numpy as np
import csv
#
logger = get_logger('month3')


def run():
    if not check_path_exist(dw_month3_summary_fpath):
        with open(dw_month3_summary_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['fromMonth', 'toMonth', 'days','numDrivers',
                             'numPickupsTotal', 'numPickupsAverage', 'numPickupsSD',
                                'numPickupsMedian', 'numPickupsMin', 'numPickupsMax',
                             'weightTotal', 'weightAverage', 'weightSD',
                                'weightMedian', 'weightMin', 'weightMax'])
    for y in range(9, 10):
        yyyy = '20%02d' % y
        yymm_fns = get_all_files(dw_graph_dir, '%s%02d' % (dw_graph_prefix, y), '.pkl')
        for i in range(len(yymm_fns) - 1):
            driver_pickup = {}
            month3_dw_graph = {}
            yymms = []
            for j in range(3):
                yymm_fn = yymm_fns[i + j]
                _, _, yymm = yymm_fn[:-len('.pkl')].split('-')
                yymms.append(yymm)
                logger.info('Loading %s' % yymm)
                month_dw_graph = load_pickle_file('%s/%s' % (dw_graph_dir, yymm_fn))
                for did0, num_pickup, weighted_link in month_dw_graph:
                    if not driver_pickup.has_key(did0):
                        driver_pickup[did0] = 0
                    driver_pickup[did0] += num_pickup
                    #
                    for did1, weight in weighted_link.iteritems():
                        k = (did0, did1)
                        if not month3_dw_graph.has_key(k):
                            month3_dw_graph[k] = 0.0
                        month3_dw_graph[k] += weight
                logger.info('Finish %s' % yymm)
            mms_str = ''.join([yymm[2:] for yymm in yymms])
            month3_dw_graph_fpath = '%s/%s%s-%s.pkl' % (dw_graph_dir, dw_graph_prefix, yyyy, mms_str)
            logger.info('Saving pickle file %s' % mms_str)
            save_pickle_file(month3_dw_graph_fpath, month3_dw_graph)
            #
            logger.info('Generate summary statistics %s' % mms_str)
            num_drivers = len(driver_pickup)
            pickups, weights = np.asarray(driver_pickup.values()), np.asarray(month3_dw_graph.values())
            month_day = set()
            for yymm in yymms:
                ft_trips_fpath = '%s/%s%s.csv' % (ft_trips_dir, ft_trips_prefix, yymm)
                with open(ft_trips_fpath, 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    headers = reader.next()
                    hid = {h: i for i, h in enumerate(headers)}
                    for row in reader:
                        day = row[hid['day']]
                        month_day.add((yymm, day))
            with open(dw_month3_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([yymms[0], yymms[1], len(month_day), num_drivers,
                                 pickups.sum(), pickups.mean(), pickups.std(),
                                    np.median(pickups), pickups.min(), pickups.max(),
                                 weights.sum(), weights.mean(), weights.std(),
                                    np.median(weights), weights.min(), weights.max()])


if __name__ == '__main__':
    run()