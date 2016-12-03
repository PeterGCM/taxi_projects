import __init__
#
'''

'''
#
from community_analysis import ss_trips_dpath, ss_trips_prefix
from community_analysis import tfZ_distribution_dpath
from community_analysis import tfZ_distribution_individuals_prefix, tfZ_distribution_groups_prefix
from community_analysis import dwg_dpath
from community_analysis import dwg_count_dpath, dwg_count_prefix
from community_analysis import dwg_benefit_dpath, dwg_benefit_prefix
from community_analysis import dwg_frequency_dpath, dwg_frequency_prefix
from community_analysis import dwg_fb_dpath, dwg_fb_prefix
from community_analysis._classes import ca_driver_with_distribution, ca_zone
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, save_pickle_file, check_dir_create, save_pkl_threading
from taxi_common.log_handling_functions import get_logger
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
from taxi_common.sg_grid_zone import get_sg_zones
#
import csv, datetime

logger = get_logger()


def run():
    logger.info('Execution')
    for dpath in [dwg_dpath, dwg_count_dpath, dwg_benefit_dpath, dwg_frequency_dpath, dwg_fb_dpath]:
        check_dir_create(dpath)
    #
    init_multiprocessor(6)
    count_num_jobs = 0
    for y in range(9, 13):
         for m in range(1, 13):
            yymm = '%02d%02d' % (y, m)
            # process_file(yymm)
            put_task(process_file, [yymm])
            count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def process_file(period):
    from traceback import format_exc
    try:
        logger.info('Handling %s' % period)
        ft_trips_fpath = '%s/%s%s.csv' % (ss_trips_dpath, ss_trips_prefix, period)
        if not check_path_exist(ft_trips_fpath):
            logger.info('No file %s' % period)
            return None
        dwg_count_fpath = '%s/%s%s.pkl' % (dwg_count_dpath, dwg_count_prefix, period)
        dwg_benefit_fpath = '%s/%s%s.pkl' % (dwg_benefit_dpath, dwg_benefit_prefix, period)
        dwg_frequency_fpath = '%s/%s%s.pkl' % (dwg_frequency_dpath, dwg_frequency_prefix, period)
        dwg_fb_fpath = '%s/%s%s.pkl' % (dwg_fb_dpath, dwg_fb_prefix, period)
        if check_path_exist(dwg_fb_fpath):
            logger.info('Already processed %s' % period)
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
        logger.info('Start %s directed weighted graph processing' % period)
        #
        individual_distribution = load_pickle_file('%s/%s%s.pkl' %
                                                   (tfZ_distribution_dpath, tfZ_distribution_individuals_prefix, period))
        group_distribution = load_pickle_file('%s/%s%s.pkl' %
                                              (tfZ_distribution_dpath, tfZ_distribution_groups_prefix, period))
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
        dwg_count, dwg_benefit, dwg_frequency, dwg_fb = [], [], [], []
        for did0, did0_obj in drivers.iteritems():
            non_zero_one_weight_link = {}
            for did1, w in did0_obj.lw_count.iteritems():
                if w < 1:
                    continue
                non_zero_one_weight_link[did1] = w
            dwg_count.append((did0, did0_obj.num_pickup, non_zero_one_weight_link))
            #
            non_zero_weight_link = {}
            for did1, w in did0_obj.lw_benefit.iteritems():
                if w == 0:
                    continue
                non_zero_weight_link[did1] = w
            dwg_benefit.append((did0, did0_obj.num_pickup, non_zero_weight_link))
            #
            non_zero_weight_link = {}
            for did1, w in did0_obj.lw_frequency.iteritems():
                if w == 0:
                    continue
                non_zero_weight_link[did1] = w
            dwg_frequency.append((did0, did0_obj.num_pickup, non_zero_weight_link))
            #
            non_zero_weight_link = {}
            for did1, w in did0_obj.lw_fb.iteritems():
                if w == 0:
                    continue
                non_zero_weight_link[did1] = w
            dwg_fb.append((did0, did0_obj.num_pickup, non_zero_weight_link))
        #
        logger.info('Start %s pickling' % period)
        save_pkl_threading(dwg_count_fpath, dwg_count)
        save_pkl_threading(dwg_benefit_fpath, dwg_benefit)
        save_pkl_threading(dwg_frequency_fpath, dwg_frequency)
        save_pickle_file(dwg_fb_fpath, dwg_fb)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], period), 'w') as f:
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
