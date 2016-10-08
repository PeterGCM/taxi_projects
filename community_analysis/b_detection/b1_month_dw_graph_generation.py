import __init__
#
from community_analysis import tf_zone_distribution_dir, tf_zone_distribution_prefix
from community_analysis import dw_graph_dir, dw_graph_prefix
from community_analysis import ft_trips_dir, ft_trips_prefix
from community_analysis._classes import ca_driver, ca_zone
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, save_pickle_file, check_dir_create
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.sg_grid_zone import get_sg_zones
#
import os, logging
import csv, datetime


def run():
    check_dir_create(dw_graph_dir)
    #
    init_multiprocessor(6)
    count_num_jobs = 0
    for y in range(9, 13):
        for m in range(1, 12):
            yymm = '%02d%02d' % (y, m)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(yymm):
    ft_trips_fpath = '%s/%s%s.csv' % (ft_trips_dir, ft_trips_prefix, yymm)
    if not check_path_exist(ft_trips_fpath):
        return None
    year_dw_graph_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_prefix, yymm)
    if check_path_exist(year_dw_graph_fpath):
        print 'The file had already been processed; %s' % yymm
        None
    #
    logger = get_logger('dw_graph')
    logger.info('Start %s directed weighted graph processing' % yymm)
    #
    yyyy = '20%s' % yymm[:2]
    year_distribution_fpath = '%s/%s%s.pkl' % (tf_zone_distribution_dir, tf_zone_distribution_prefix, yyyy)
    year_distribution = load_pickle_file(year_distribution_fpath)
    logger.info('Finish year distribution loading')
    #
    drivers = {}
    zones = generate_zones()
    handling_day = 0
    with open(ft_trips_fpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        for row in reader:
            t = eval(row[hid['time']])
            cur_dt = datetime.datetime.fromtimestamp(t)
            if handling_day != cur_dt.day:
                logger.info('Processing %dth day' % cur_dt.day)
                handling_day = cur_dt.day
            did = int(row[hid['did']])
            zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
            try:
                z = zones[(zi, zj)]
            except KeyError:
                continue
            if not drivers.has_key(did):
                drivers[did] = ca_driver(did, year_distribution[did])
            drivers[did].update_linkage(t, z)
    logger.info('Start %s aggregation' % yymm)
    year_dw_graph = []
    for did, d in drivers.iteritems():
        year_dw_graph.append((did, d.num_pickup, d.weighted_link))
    logger.info('Start %s pickling' % yymm)
    save_pickle_file(year_dw_graph_fpath, year_dw_graph)


def generate_zones():
    zones = {}
    basic_zones = get_sg_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = ca_zone(z.relation_with_poly, z.zi, z.zj, z.cCoor_gps, z.polyPoints_gps)
    return zones


if __name__ == '__main__':
    run()