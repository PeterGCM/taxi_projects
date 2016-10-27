import __init__
#
from community_analysis import ss_trips_dir, ss_trips_prefix
from community_analysis import tf_zone_distribution_dir
from community_analysis import tf_zone_distribution_individuals_prefix, tf_zone_distribution_groups_prefix
from community_analysis import dw_graph_dir, dw_graph_prefix
from community_analysis._classes import ca_driver_with_distribution, ca_zone
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, save_pickle_file, check_dir_create
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.sg_grid_zone import get_sg_zones
#
import csv, datetime

logger = get_logger('dw_graph')


def run():
    logger.info('Execution')
    check_dir_create(dw_graph_dir)
    #
    init_multiprocessor(6)
    count_num_jobs = 0
    for y in range(9, 13):
        yyyy = '20%02d' % (y)
        # process_file(yyyy)
        put_task(process_file, [yyyy])
        count_num_jobs += 1
        for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(period):
    from traceback import format_exc
    try:
        logger.info('Handling %s' % period)
        ft_trips_fpath = '%s/%s%s.csv' % (ss_trips_dir, ss_trips_prefix, period)
        if not check_path_exist(ft_trips_fpath):
            logger.info('No file %s' % period)
            return None
        did_gn = {}
        with open(ft_trips_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            for row in reader:
                did = int(row[hid['did']])
                gn = row[hid['groupName']]
                if did_gn.has_key(did):
                    assert did_gn[did] == gn, (did, gn)
                    continue
                else:
                    did_gn[did] = gn
        #
        dw_graph_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_prefix, period)
        if check_path_exist(dw_graph_fpath):
            logger.info('Already processed %s' % period)
            return None
        logger.info('Start %s directed weighted graph processing' % period)
        #
        individual_distribution = load_pickle_file('%s/%s%s.pkl' %
                                       (tf_zone_distribution_dir, tf_zone_distribution_individuals_prefix, period))
        group_distribution = load_pickle_file('%s/%s%s.pkl' %
                                                   (tf_zone_distribution_dir, tf_zone_distribution_groups_prefix, period))
        logger.info('Finish distribution loading')
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
                    logger.info('Processing %s %dth day (month %d)' % (period, cur_dt.day, cur_dt.month))
                    for d in drivers.itervalues():
                        d.update_linkFrequency()
                    handling_day = cur_dt.day
                did = int(row[hid['did']])
                zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                try:
                    z = zones[(zi, zj)]
                except KeyError:
                    continue
                if not individual_distribution.has_key(did):
                    continue
                if not drivers.has_key(did):
                    drivers[did] = ca_driver_with_distribution(did, individual_distribution[did],
                                                               group_distribution[did_gn[did]])
                drivers[did].update_linkWeight(t, z)
        logger.info('Start %s aggregation' % period)
        dw_graph = []
        for did, d in drivers.iteritems():
            non_zero_weight_link = {}
            for did0, w in d.link_weight.iteritems():
                if w == 0:
                    continue
                non_zero_weight_link[did0] = w
            dw_graph.append((did, d.num_pickup, non_zero_weight_link))
        logger.info('Start %s pickling' % period)
        save_pickle_file(dw_graph_fpath, dw_graph)
    except Exception as _:
        with open('Exception month dw graph.txt', 'w') as f:
            f.write(format_exc())
        raise


def generate_zones():
    zones = {}
    basic_zones = get_sg_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = ca_zone(z.relation_with_poly, z.zi, z.zj, z.cCoor_gps, z.polyPoints_gps)
    return zones


if __name__ == '__main__':
    run()
