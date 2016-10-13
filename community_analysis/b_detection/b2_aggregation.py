import __init__
#
from community_analysis import ft_trips_dir, ft_trips_prefix
from community_analysis import dw_graph_dir, dw_graph_prefix
from community_analysis import dw_aggreg_dir, dw_aggreg_prefix
from community_analysis import year_aggre_summary_fpath, month3_aggre_summary_fpath
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, save_pickle_file, \
    get_all_files, save_pkl_threading, check_dir_create
from taxi_common.log_handling_functions import get_logger
#
import numpy as np
import csv
#
logger = get_logger('aggregation')


def run():
    check_dir_create(dw_aggreg_dir)
    if not check_path_exist(year_aggre_summary_fpath):
        with open(year_aggre_summary_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'days','numDrivers',
                                'numPickupsTotal', 'numPickupsAverage', 'numPickupsSD',
                                'numPickupsMedian', 'numPickupsMin', 'numPickupsMax',
                             'numLinks',
                                'weightTotal', 'weightAverage', 'weightSD',
                                'weightMedian', 'weightMin', 'weightMax'])
    if not check_path_exist(month3_aggre_summary_fpath):
        with open(month3_aggre_summary_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['year', 'months', 'days', 'numDrivers',
                                'numPickupsTotal', 'numPickupsAverage', 'numPickupsSD',
                                'numPickupsMedian', 'numPickupsMin', 'numPickupsMax',
                             'numLinks',
                                'weightTotal', 'weightAverage', 'weightSD',
                                'weightMedian', 'weightMin', 'weightMax'])

    for y in range(9, 13):
        yyyy = '20%02d' % y
        logger.info('Handle %s' % yyyy)
        year_aggregation_fpath = '%s/%s%s.pkl' % (dw_aggreg_dir, dw_aggreg_prefix, yyyy)
        year_driver_pickup, year_dw_graph = {}, {}
        year_days = set()
        for m in range(1, 13):
            month3_driver_pickup, month3_dw_graph = {}, {}
            month3_days = set()
            yymm = '%02d%02d' % (y, m)
            logger.info('Loading %s' % yymm)
            month_dw_graph_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_prefix, yymm)
            if not check_path_exist(month_dw_graph_fpath):
                continue
            #
            ft_trips_fpath = '%s/%s%s.csv' % (ft_trips_dir, ft_trips_prefix, yymm)
            with open(ft_trips_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    day = row[hid['day']]
                    year_days.add((m, day))
                    month3_days.add((m, day))
            #
            month_dw_graph = load_pickle_file(month_dw_graph_fpath)
            for did0, num_pickup, weighted_link in month_dw_graph:
                if not year_driver_pickup.has_key(did0):
                    year_driver_pickup[did0] = 0
                if not month3_driver_pickup.has_key(did0):
                    month3_driver_pickup[did0] = 0
                year_driver_pickup[did0] += num_pickup
                month3_driver_pickup[did0] += num_pickup
                #
                for did1, weight in weighted_link.iteritems():
                    k = (did0, did1)
                    if not year_dw_graph.has_key(k):
                        year_dw_graph[k] = 0.0
                    if not month3_dw_graph.has_key(k):
                        month3_dw_graph[k] = 0.0
                    year_dw_graph[k] += weight
                    month3_dw_graph[k] += weight
            #
            yymm_fns = get_all_files(dw_graph_dir, '%s%02d' % (dw_graph_prefix, y), '.pkl')
            rolling_horizon_lm = m
            yymms, next_month_fns = [yymm], []
            for yymm_fn in yymm_fns:
                _, _, n_yymm = yymm_fn[:-len('.pkl')].split('-')
                target_m = int(n_yymm[2:])
                if rolling_horizon_lm < target_m:
                    next_month_fns.append(yymm_fn)
                    yymms.append(n_yymm)
                    #
                    ft_trips_fpath = '%s/%s%s.csv' % (ft_trips_dir, ft_trips_prefix, n_yymm)
                    with open(ft_trips_fpath, 'rb') as r_csvfile:
                        reader = csv.reader(r_csvfile)
                        headers = reader.next()
                        hid = {h: i for i, h in enumerate(headers)}
                        for row in reader:
                            day = row[hid['day']]
                            month3_days.add((m, day))
                    rolling_horizon_lm = target_m
                if len(yymms) == 3:
                    break
            if len(yymms) < 3:
                continue
            for yymm_fn in next_month_fns:
                logger.info('Loading %s for rolling horizon' % yymm_fn)
                month_dw_graph1 = load_pickle_file('%s/%s' % (dw_graph_dir, yymm_fn))
                for did0, num_pickup, weighted_link in month_dw_graph1:
                    if not month3_driver_pickup.has_key(did0):
                        month3_driver_pickup[did0] = 0
                    month3_driver_pickup[did0] += num_pickup
                    #
                    for did1, weight in weighted_link.iteritems():
                        k = (did0, did1)
                        if not month3_dw_graph.has_key(k):
                            month3_dw_graph[k] = 0.0
                        month3_dw_graph[k] += weight
                logger.info('Finish %s for rolling horizon' % yymm_fn)

            month3_str = ''.join(['M%s' % yymm[2:] for yymm in yymms])
            month3_aggregation_fpath = '%s/%s%s-%s.pkl' % (dw_aggreg_dir, dw_aggreg_prefix, yyyy, month3_str)
            logger.info('Saving pickle file %s' % month3_str)
            save_pkl_threading(month3_aggregation_fpath, month3_dw_graph)
            #
            logger.info('Generate month3 summary statistics %s' % yyyy)
            num_drivers = len(month3_driver_pickup)
            num_links = len(month3_dw_graph)
            pickups, weights = np.asarray(month3_driver_pickup.values()), np.asarray(month3_dw_graph.values())
            with open(month3_aggre_summary_fpath, 'a') as w_csvfile:
                writer = csv.writer(w_csvfile, lineterminator='\n')
                writer.writerow([yyyy, month3_str, len(month3_days), num_drivers,
                                 pickups.sum(), pickups.mean(), pickups.std(),
                                    np.median(pickups), pickups.min(), pickups.max(),
                                 num_links,
                                    weights.sum(), weights.mean(), weights.std(),
                                    np.median(weights), weights.min(), weights.max()])
        logger.info('Saving year_dw_graph0 %s' % yyyy)
        save_pickle_file(year_aggregation_fpath, year_dw_graph)
        #
        logger.info('Generate year summary statistics %s' % yyyy)
        num_drivers = len(year_driver_pickup)
        num_links = len(year_dw_graph)
        pickups, weights = np.asarray(year_driver_pickup.values()), np.asarray(year_dw_graph.values())
        with open(year_aggre_summary_fpath, 'a') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow([yyyy, len(year_days), num_drivers,
                                pickups.sum(), pickups.mean(), pickups.std(),
                                np.median(pickups), pickups.min(), pickups.max(),
                             num_links,
                                weights.sum(), weights.mean(), weights.std(),
                                np.median(weights), weights.min(), weights.max()])

if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception aggregation.txt', 'w') as f:
            f.write(format_exc())
        raise
