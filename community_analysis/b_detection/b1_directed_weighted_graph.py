import __init__
#
from community_analysis import tf_zone_distribution_dir, tf_zone_distribution_prefix
from community_analysis import dw_graph_dir, dw_graph_prefix
from community_analysis import ft_trips_dir
from community_analysis._classes import ca_driver, ca_zone
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, get_all_files, save_pickle_file
from taxi_common.sg_grid_zone import get_sg_zones
#
import csv


def run():
    for y in range(9, 13):
        yyyy = '20%02d' % y
        print 'Handle %s' % yyyy
        year_dw_graph_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_prefix, yyyy)
        if check_path_exist(year_dw_graph_fpath):
            print 'The file had already been processed; %s' % yyyy
            continue
        year_distribution_fpath = '%s/%s%s.pkl' % (tf_zone_distribution_dir, tf_zone_distribution_prefix, yyyy)
        year_distribution = load_pickle_file(year_distribution_fpath)
        for fn in get_all_files(ft_trips_dir, '', '.csv'):
            _, _, _, yymm = fn[:-len('.csv')].split('-')
            if not yymm.startwith('%02d' % y):
                continue
            drivers = {}
            zones = generate_zones()
            print 'Handling %s' % yymm
            with open('%s/%s' % (ft_trips_dir, fn), 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    t = eval(row[hid['time']])
                    did = int(row[hid['did']])
                    zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                    try:
                        z = zones[(zi, zj)]
                    except KeyError:
                        continue
                    if not drivers.has_key(did):
                        drivers[did] = ca_driver(did, year_distribution[did])
                    drivers[did].update_linkage(t, z)
        print 'Aggregation %s' % yyyy
        year_dw_graph = []
        for did, d in drivers.iteritems():
            year_dw_graph.append((did, d.num_pickup, d.weighted_link))
        save_pickle_file(year_dw_graph_fpath, year_dw_graph)


def generate_zones():
    zones = {}
    basic_zones = get_sg_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = ca_zone(z.relation_with_poly, z.i, z.j, z.cCoor_gps, z.polyPoints_gps)
    return zones

if __name__ == '__main__':
    run()