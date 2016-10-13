import __init__
#
from community_analysis import ft_trips_dir, ft_trips_prefix
from community_analysis import dw_graph_dir, dw_graph_prefix, dw_graph_above_avg_prefix, \
    dw_graph_above_per90_prefix, dw_graph_above_per95_prefix, dw_graph_above_per99_prefix, \
    dw_graph_above_per999_prefix
from community_analysis import month3_aggre_summary_fpath, dw_month3_summary_fpath1, dw_month3_summary_fpath2
#
from taxi_common.file_handling_functions import load_pickle_file, check_path_exist, save_pickle_file, get_all_files
from taxi_common.log_handling_functions import get_logger
#
import numpy as np
import csv
#
logger = get_logger('month3')


def run():
    # threshold_values = list(np.arange(99.9, 100, 0.01))
    # with open(dw_month3_summary_fpath2, 'wt') as w_csvfile:
    #     writer = csv.writer(w_csvfile, lineterminator='\n')
    #     new_row = ['year', 'months', 'days', 'numDrivers',
    #                         'numPickupsTotal', 'numPickupsAverage', 'numPickupsSD',
    #                         'numPickupsMedian', 'numPickupsMin', 'numPickupsMax',
    #                      'numLinks',
    #                         'weightTotal', 'weightAverage', 'weightSD',
    #                         'weightMedian', 'weightMin', 'weightMax']
    #     for th in threshold_values:
    #         new_row.append('weightPer%.2f' % th)
    #     writer.writerow(new_row)
    # print new_row
    # assert False


    # if not check_path_exist(dw_month3_summary_fpath):
    # with open(dw_month3_summary_fpath, 'wt') as w_csvfile:
    #     writer = csv.writer(w_csvfile, lineterminator='\n')
    #     writer.writerow(['year', 'months', 'days', 'numDrivers',
    #                         'numPickupsTotal', 'numPickupsAverage', 'numPickupsSD',
    #                         'numPickupsMedian', 'numPickupsMin', 'numPickupsMax',
    #                      'numLinks',
    #                         'weightTotal', 'weightAverage', 'weightSD',
    #                         'weightMedian', 'weightMin', 'weightMax', 'weightPer90', 'weightPer95'])

    for y in range(11, 13):
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
            month3_str = ''.join(['M%s' % yymm[2:] for yymm in yymms])
            month3_dw_graph0_fpath = '%s/%s%s-%s.pkl' % (dw_graph_dir, dw_graph_prefix, yyyy, month3_str)
            logger.info('Saving pickle file %s' % month3_str)
            save_pickle_file(month3_dw_graph0_fpath, month3_dw_graph)
            #
            # month3_dw_graph1_fpath = '%s/%s%s-%s.pkl' % (dw_graph_dir, dw_graph_above_avg_prefix, yyyy, month3_str)
            # weight_avg = np.asarray(month3_dw_graph.values()).mean()
            # month3_dw_graph_above_avg = {k: v for k, v in month3_dw_graph.iteritems() if v > weight_avg}
            # save_pickle_file(month3_dw_graph1_fpath, month3_dw_graph_above_avg)
            # #
            # month3_dw_graph2_fpath = '%s/%s%s-%s.pkl' % (dw_graph_dir, dw_graph_above_per90_prefix, yyyy, month3_str)
            # percentile90 = np.percentile(month3_dw_graph.values(), 90)
            # year_dw_graph_above_per90 = {k: v for k, v in month3_dw_graph.iteritems() if v > percentile90}
            # save_pickle_file(month3_dw_graph2_fpath, year_dw_graph_above_per90)
            # #
            # month3_dw_graph3_fpath = '%s/%s%s-%s.pkl' % (dw_graph_dir, dw_graph_above_per95_prefix, yyyy, month3_str)
            # percentile95 = np.percentile(month3_dw_graph.values(), 95)
            # year_dw_graph_above_per95 = {k: v for k, v in month3_dw_graph.iteritems() if v > percentile95}
            # save_pickle_file(month3_dw_graph3_fpath, year_dw_graph_above_per95)
            #
            # month3_dw_graph3_fpath = '%s/%s%s-%s.pkl' % (dw_graph_dir, dw_graph_above_per99_prefix, yyyy, month3_str)
            # percentile99 = np.percentile(month3_dw_graph.values(), 99)
            # year_dw_graph_above_per99 = {k: v for k, v in month3_dw_graph.iteritems() if v > percentile99}
            # save_pickle_file(month3_dw_graph3_fpath, year_dw_graph_above_per99)
            #
            # month3_dw_graph3_fpath = '%s/%s%s-%s.pkl' % (dw_graph_dir, dw_graph_above_per999_prefix, yyyy, month3_str)
            # percentile999 = np.percentile(month3_dw_graph.values(), 99.9)
            # year_dw_graph_above_per999 = {k: v for k, v in month3_dw_graph.iteritems() if v > percentile999}
            # save_pickle_file(month3_dw_graph3_fpath, year_dw_graph_above_per999)
            # #
            # logger.info('Generate summary statistics %s' % month3_str)
            # num_drivers = len(driver_pickup)
            # num_links = len(month3_dw_graph)
            # pickups, weights = np.asarray(driver_pickup.values()), np.asarray(month3_dw_graph.values())
            # month_day = set()
            # for yymm in yymms:
            #     with open('%s/%s%s.csv' % (ft_trips_dir, ft_trips_prefix, yymm), 'rb') as r_csvfile:
            #         reader = csv.reader(r_csvfile)
            #         headers = reader.next()
            #         hid = {h: i for i, h in enumerate(headers)}
            #         for row in reader:
            #             day = row[hid['day']]
            #             month_day.add((yymm, day))
            # with open(dw_month3_summary_fpath1, 'a') as w_csvfile:
            #     writer = csv.writer(w_csvfile, lineterminator='\n')
            #     writer.writerow([yyyy, month3_str, len(month_day), num_drivers,
            #                      pickups.sum(), pickups.mean(), pickups.std(),
            #                         np.median(pickups), pickups.min(), pickups.max(),
            #                      num_links,
            #                         weights.sum(), weights.mean(), weights.std(),
            #                         np.median(weights), weights.min(), weights.max(), year_dw_graph_above_per999])


if __name__ == '__main__':
    from traceback import format_exc
    #
    try:
        run()
    except Exception as _:
        with open('Exception month3.txt', 'w') as f:
            f.write(format_exc())
        raise