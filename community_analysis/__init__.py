import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'; check_dir_create(taxi_data)
#
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
PM2, PM11 = 14, 23
THRESHOLD_VALUE = 30 * 60
#
ss_trips_dir = '%s/%s' % (taxi_data, 'trips_ss_drivers'); ss_trips_prefix = 'trips-ss-drivers-'
tf_zone_counting_dir = '%s/%s' % (taxi_data, 'tf_zone_counting'); tf_zone_counting_prefix = 'tf-zone-counting-'
tf_zone_distribution_dir = '%s/%s' % (taxi_data, 'tf_zone_distribution'); tf_zone_distribution_prefix = 'tf-zone-distribution-'
#
DEPRECIATION_LAMBDA = 0.5
dw_graph_dir = '%s/%s' % (taxi_data, 'dw_graph'); dw_graph_prefix = 'dw-graph-'
dw_aggreg_dir = '%s/%s' % (dw_graph_dir, 'dw_aggregation'); dw_aggreg_prefix = 'dw-aggregation-'
year_aggre_summary_fpath = '%s/%s.csv' % (dw_aggreg_dir, 'year-aggretation-summary')
month3_aggre_summary_fpath = '%s/%s.csv' % (dw_aggreg_dir, 'month3-aggretation-summary')
dw_filtered_dir = '%s/%s' % (dw_graph_dir, 'dw_filtered'); dw_filtered_prefix = 'dw-filtered-'
group_dir = '%s/%s' % (taxi_data, 'group'); group_prepix = 'group-'
group_summary_fpath = '%s/%s.csv' % (group_dir , 'group-summary')
#
CHOSEN_PERCENTILE = 99.995
MIN_NUM_DRIVERS = 10
com_drivers_dir = '%s/%s' % (taxi_data, 'com_drivers'); com_drivers_prefix = 'com-drivers-'
com_trips_dir = '%s/%s' % (taxi_data, 'com_trips'); com_trips_prefix = 'com-trips-'



dw_graph_above_avg_prefix = 'dw-graph-above-avg-'
dw_graph_above_per75_prefix = 'dw-graph-above-per75-'
dw_graph_above_per90_prefix = 'dw-graph-above-per90-'
dw_graph_above_per95_prefix = 'dw-graph-above-per95-'
dw_graph_above_per95_prefix = 'dw-graph-above-per95-'
dw_graph_above_per99_prefix = 'dw-graph-above-per99-'
dw_graph_above_per999_prefix = 'dw-graph-above-per990-'
dw_graph_per_prefix = 'dw-graph-above-per-'




dw_month3_summary_fpath1 = '%s/%s.csv' % (dw_graph_dir, 'dw-month3-summary1')
dw_month3_summary_fpath2 = '%s/%s.csv' % (dw_graph_dir, 'dw-month3-summary2')

group_summary_fpath = '%s/%s.csv' % (group_dir, 'group-summary')


# trip_dir = '%s/%s' % (taxi_data, 'trips')
# ld_dir = '%s/%s' % (taxi_data, 'linkage_daily')
# lm_dir = '%s/%s' % (taxi_data, 'linkage_monthly')
# la_dir = '%s/%s' % (taxi_data, 'linkage_annually')
# com_dir = '%s/%s' % (taxi_data, 'community')
# com_summary_2009_fpath = '%s/%s' % (com_dir, '2009-com_summary.csv')
# #
# top5_com_dir = '%s/%s' % (taxi_data, 'top5_community')
# ctrip_dir = '%s/%s' % (taxi_data, 'ctrips')
# clink_dir = '%s/%s' % (taxi_data, 'clinks')
# cevol_dir = '%s/%s' % (taxi_data, 'cevol')
# #
# all_trip_dir, all_trip_prefix = '%s/%s' % (taxi_data, 'all_trips'), 'all-trips-'
# year_dist_dir = '%s/%s' % (taxi_data, 'ydists')
# individual_dist_fpath = '%s/%s' % (year_dist_dir, 'individual_dist.pkl')
# individual_couting_fpath = '%s/%s' % (year_dist_dir, 'individual_counting.pkl')
# trip_likelihood_fpath = '%s/%s' % (all_trip_dir, '2009-trip_likelihood.csv')
#
#
# com_trip_dir = '%s/%s' % (taxi_data, 'com_trips')
# lm_dg_dir = '%s/%s' % (taxi_data, 'month_directional')



# pg_dir = taxi_data + '/partitioned_group'; check_dir_create(pg_dir)
#
# com_trip_dir = taxi_data + '/ctrips'; check_dir_create(com_trip_dir)
#
# com_log_dir = taxi_data + '/com_logs'; check_dir_create(com_log_dir)
# com_linkage_dir = taxi_data + '/com_linkage'; check_dir_create(com_linkage_dir)
# cevol_dir = taxi_data + '/cevol'; check_dir_create(cevol_dir)

#
# MIN_DAILY_LINKAGE = 2
#
# THRESHOLD_VALUE = 30 * 60
# BY_COM_O, BY_COM_X = 'O', 'X'

#
# from community_analysis._classes import ca_zone
# from taxi_common.sg_grid_zone import get_sg_zones
#
#
# def generate_zones():
#     zones = {}
#     basic_zones = get_sg_zones()
#     for k, z in basic_zones.iteritems():
#         zones[k] = ca_zone(z.relation_with_poly, z.i, z.j, z.cCoor_gps, z.polyPoints_gps)
#     return zones