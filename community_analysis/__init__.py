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
ss_trips_dpath = '%s/%s' % (taxi_data, 'trips_ss_drivers'); ss_trips_prefix = 'trips-ss-drivers-'
tfZ_counting_dpath = '%s/%s' % (taxi_data, 'tf_zone_counting')
tfZ_counting_individuals_prefix = 'tf-zone-counting-individuals-'
tfZ_counting_groups_prefix = 'tf-zone-counting-groups-'
tfZ_distribution_dpath = '%s/%s' % (taxi_data, 'tf_zone_distribution')
tfZ_distribution_individuals_prefix = 'tf-zone-distribution-individuals-'
tfZ_distribution_groups_prefix = 'tf-zone-distribution-groups-'
tfZ_distribution_whole_prefix = 'tf-zone-distribution-whole-'
#
DEPRECIATION_LAMBDA = 0.5
dwg_dpath = '%s/%s' % (taxi_data, 'dw_graph'); dwg_prefix = 'dw-graph-'
dwg_count_dpath = '%s/%s' % (dwg_dpath, 'count'); dwg_count_prefix = 'dw-graph-count-'
dwg_benefit_dpath = '%s/%s' % (dwg_dpath, 'benefit'); dwg_benefit_prefix = 'dw-graph-benefit-'
dwg_frequency_dpath = '%s/%s' % (dwg_dpath, 'frequency'); dwg_frequency_prefix = 'dw-graph-frequency-'
dwg_fb_dpath = '%s/%s' % (dwg_dpath, 'fb'); dwg_fb_prefix = 'dw-graph-fb-'
dwg_summary_fpath = '%s/%s' % (dwg_dpath, 'dwg-summary.csv')
TOPZPZ1PERCENT = 0.0001
CHOSEN_PERCENT = TOPZPZ1PERCENT
fdwg_dpath = '%s/%s' % (taxi_data, 'fdw_graph(%.4f)' % CHOSEN_PERCENT); fdw_graph_prefix = 'fdw-graph-'
group_dpath = '%s/%s' % (taxi_data, 'group(%.4f)' % CHOSEN_PERCENT); group_prepix = 'group-'
group_summary_fpath = '%s/%s.csv' % (group_dpath , 'group-summary')
#
pickUp_dpath = '%s/%s' % (taxi_data, 'pickUp'); pickUp_prepix = 'pickUp-'
roamingTime_dpath = '%s/%s' % (taxi_data, 'roamingTime'); roamingTime_prepix = 'roamingTime-'
regressionModel_dpath = '%s/%s' % (taxi_data, 'regressionModel'); regressionModel_prepix = 'regressionModel-'
X_PICKUP, O_PICKUP = range(2)





MIN_NUM_DRIVERS = 10



#



#
FREE = 0
roaming_time_dir = '%s/%s' % (taxi_data, 'roaming_time'); roaming_time_prefix = 'roaming-time-'
rt_day_dir = '%s/%s' % (roaming_time_dir, 'day'); rt_day_prefix = 'roaming-time-day-'
tf_zone_drivers_dir = '%s/%s' % (taxi_data, 'tf_zone_drivers'); tf_zone_drivers_prefix = 'tf-zone-drivers-'
X_APPEAR, O_APPEAR = range(2)
rt_appear_dir = '%s/%s' % (taxi_data, 'rt_appear'); rt_appear_prefix = 'rt-appear-'




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
