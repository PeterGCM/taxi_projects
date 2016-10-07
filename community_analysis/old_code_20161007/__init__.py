import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'; check_dir_create(taxi_data)
#
trip_dir = '%s/%s' % (taxi_data, 'trips')
ld_dir = '%s/%s' % (taxi_data, 'linkage_daily')
lm_dir = '%s/%s' % (taxi_data, 'linkage_monthly')
la_dir = '%s/%s' % (taxi_data, 'linkage_annually')
com_dir = '%s/%s' % (taxi_data, 'community')
com_summary_2009_fpath = '%s/%s' % (com_dir, '2009-com_summary.csv')
#
top5_com_dir = '%s/%s' % (taxi_data, 'top5_community')
ctrip_dir = '%s/%s' % (taxi_data, 'ctrips')
clink_dir = '%s/%s' % (taxi_data, 'clinks')
cevol_dir = '%s/%s' % (taxi_data, 'cevol')
#
all_trip_dir, all_trip_prefix = '%s/%s' % (taxi_data, 'all_trips'), 'all-trips-'
year_dist_dir = '%s/%s' % (taxi_data, 'ydists')
individual_dist_fpath = '%s/%s' % (year_dist_dir, 'individual_dist.pkl')
individual_couting_fpath = '%s/%s' % (year_dist_dir, 'individual_counting.pkl')
trip_likelihood_fpath = '%s/%s' % (all_trip_dir, '2009-trip_likelihood.csv')


com_trip_dir = '%s/%s' % (taxi_data, 'com_trips')
lm_dg_dir = '%s/%s' % (taxi_data, 'month_directional')



# pg_dir = taxi_data + '/partitioned_group'; check_dir_create(pg_dir)
#
# com_trip_dir = taxi_data + '/ctrips'; check_dir_create(com_trip_dir)
#
# com_log_dir = taxi_data + '/com_logs'; check_dir_create(com_log_dir)
# com_linkage_dir = taxi_data + '/com_linkage'; check_dir_create(com_linkage_dir)
# cevol_dir = taxi_data + '/cevol'; check_dir_create(cevol_dir)

#
MIN_DAILY_LINKAGE = 2
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
PM2, PM3 = 14, 15
PM11 = 23
THRESHOLD_VALUE = 30 * 60
BY_COM_O, BY_COM_X = 'O', 'X'

#
from community_analysis._classes import ca_zone
from taxi_common.sg_grid_zone import get_sg_zones


def generate_zones():
    zones = {}
    basic_zones = get_sg_zones()
    for k, z in basic_zones.iteritems():
        zones[k] = ca_zone(z.relation_with_poly, z.i, z.j, z.cCoor_gps, z.polyPoints_gps)
    return zones