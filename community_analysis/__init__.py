import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'; check_dir_create(taxi_data)
chart_dpath = os.path.dirname(os.path.realpath(__file__)) + '/chart'; check_dir_create(chart_dpath)
shift_dpath, shift_prefix = '/home/sfcheng/toolbox/results', 'shift-hour-state-'
#
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
PM2, PM11 = 14, 23
THRESHOLD_VALUE = 30 * 60
FREE, POB = 0, 5
MIN20 = 20 * 60.0
X_PRESENCE, O_PRESENCE = range(2)
#
SIGINIFICANCE_LEVEL = 0.05
MIN_PICKUP_RATIO = 0.1
MIN_NUM_TRIPS_MONTH = 5
#
years = ['20%02d' % y for y in range(9, 13)]
#
ss_trips_dpath, ss_trips_prefix = '%s/%s' % (taxi_data, 'trips_ss_drivers'), 'trips-ss-drivers-'
prevDriversDefined_dpath, prevDriversDefined_prefix =  '%s/%s' % (taxi_data, 'prevDriversDefined'), 'prevDriversDefined-'
tfZ_TP_dpath, tfZ_TP_prefix = '%s/%s' % (taxi_data, 'tfZ_TP'), 'tfZ_TP-'
driversRelations_fpaths = {year: '%s/driversRelations%s.pkl' % (prevDriversDefined_dpath, year) for year in years}
#
timeMeasures = ['spendingTime', 'roamingTime']
interResults = ['influenceGraph', 'groupPartition', 'groupTrips', 'groupShifts','groupZones', 'groupMarginal']
dpaths, prefixs = {}, {}
for tm in timeMeasures:
    for year in years:
        for ir in interResults:
            dpaths[tm, year, ir] = '%s/%s/%s/%s' % (taxi_data, tm, year, ir)
            prefixs[tm, year, ir] = '%s-%s-%s-' % (tm, year, ir)

groupPartitionSummaries, groupPartitionDrivers = {}, {}
for tm in timeMeasures:
    for year in years:
        groupPartition_dpath = dpaths[tm, year, 'groupPartition']
        groupPartition_prefix = prefixs[tm, year, 'groupPartition']
        groupPartitionSummaries[tm, year] = '%s/%s' % (groupPartition_dpath, groupPartition_prefix)






group_dpath = '%s/%s' % (taxi_data, 'group')
SP_group_dpath, SP_group_prefix = '%s/%s' % (group_dpath, 'SP_group'), 'SP-group-'
SP_group_drivers_fpath = '%s/%s' % (SP_group_dpath, 'SP-group-drivers.pkl')
SP_group_summary_fpath = '%s/%s' % (SP_group_dpath, 'SP-group-summary.csv')
RP_group_dpath, RP_group_prefix = '%s/%s' % (group_dpath, 'RP_group'), 'RP-group-'
RP_group_drivers_fpath = '%s/%s' % (RP_group_dpath, 'RP-group-drivers.pkl')
RP_group_summary_fpath = '%s/%s' % (RP_group_dpath, 'RP-group-summary.csv')
#
SP_groupDefinedTrip_dpath, SP_groupDefinedTrip_prefix = '%s/%s' % (taxi_data, 'SP-groupDefinedTrip'), 'SP-groupDefinedTrip-'
RP_groupDefinedTrip_dpath, RP_groupDefinedTrip_prefix = '%s/%s' % (taxi_data, 'RP-groupDefinedTrip'), 'RP-groupDefinedTrip-'
#
comZones_dpath = '%s/%s' % (taxi_data, 'comZones')
SP_comZones_dpath, SP_comZones_prefix = '%s/%s' % (comZones_dpath, 'SP_comZones'), 'SP-comZones-'
RP_comZones_dpath, RP_comZones_prefix = '%s/%s' % (comZones_dpath, 'RP_comZones'), 'RP-comZones-'
SP_interesting_zone_fpath = '%s/SP-zone-summary.pkl' % SP_comZones_dpath
RP_interesting_zone_fpath = '%s/RP-zone-summary.pkl' % RP_comZones_dpath
#
#
# tfZ_pickUp_dpath, tfZ_pickUp_prepix = '%s/%s' % (taxi_data, 'tfZ_pickUp'), 'tfZ-pickUp-'
# tfZ_spendingTime_dpath, tfZ_spendingTime_prepix = '%s/%s' % (taxi_data, 'tfZ_spendingTime'), 'tfZ-spendingTime-'
# tfZ_SP_dpath, tfZ_SP_prepix = '%s/%s' % (taxi_data, 'tfZ_SP'), 'tfZ-SP-'
# tfZ_roamingTime_dpath, tfZ_roamingTime_prefix = '%s/%s' % (taxi_data, 'tfZ_roamingTime'), 'tfZ-roamingTime-'
# tfZ_RP_dpath, tfZ_RP_prepix = '%s/%s' % (taxi_data, 'tfZ_RP'), 'tfZ-RP-'
#
#
#
#
# RP_group_dpath, RP_group_prefix = '%s/%s' % (taxi_data, 'RP_group'), 'RP-group-'
# RP_group_drivers_fpath = '%s/%s' % (RP_group_dpath, 'RP-group-drivers.pkl')
# RP_group_summary_fpath = '%s/%s' % (RP_group_dpath, 'RP-group-summary.csv')
#
#
#
#
# tfZ_counting_dpath = '%s/%s' % (taxi_data, 'tf_zone_counting')
# tfZ_counting_individuals_prefix = 'tf-zone-counting-individuals-'
# tfZ_counting_groups_prefix = 'tf-zone-counting-groups-'
# tfZ_distribution_dpath = '%s/%s' % (taxi_data, 'tf_zone_distribution')
# tfZ_distribution_individuals_prefix = 'tf-zone-distribution-individuals-'
# tfZ_distribution_groups_prefix = 'tf-zone-distribution-groups-'
# tfZ_distribution_whole_prefix = 'tf-zone-distribution-whole-'
# #
# DEPRECIATION_LAMBDA = 0.5
# dwg_dpath = '%s/%s' % (taxi_data, 'dw_graph'); dwg_prefix = 'dw-graph-'
# dwg_count_dpath = '%s/%s' % (dwg_dpath, 'count'); dwg_count_prefix = 'dw-graph-count-'
# dwg_benefit_dpath = '%s/%s' % (dwg_dpath, 'benefit'); dwg_benefit_prefix = 'dw-graph-benefit-'
# dwg_frequency_dpath = '%s/%s' % (dwg_dpath, 'frequency'); dwg_frequency_prefix = 'dw-graph-frequency-'
# dwg_fb_dpath = '%s/%s' % (dwg_dpath, 'fb'); dwg_fb_prefix = 'dw-graph-fb-'
# dwg_summary_fpath = '%s/%s' % (dwg_dpath, 'dwg-summary.csv')
# TOPZPZ1PERCENT = 0.0001
# CHOSEN_PERCENT = TOPZPZ1PERCENT
# fdwg_dpath = '%s/%s' % (taxi_data, 'fdw_graph(%.4f)' % CHOSEN_PERCENT); fdw_graph_prefix = 'fdw-graph-'
# group_dpath = '%s/%s' % (taxi_data, 'group(%.4f)' % CHOSEN_PERCENT); group_prepix = 'group-'
# group_summary_fpath = '%s/%s.csv' % (group_dpath , 'group-summary')
# #
#
#
#
# pickUpY2_dpath = '%s/%s' % (taxi_data, 'pickUpY2'); pickUpY2_prepix = 'pickUpY2-'
#
# roamingTime_dpath = '%s/%s' % (taxi_data, 'roamingTime'); roamingTime_prepix = 'roamingTime-'
# roamingTimeY2_dpath = '%s/%s' % (taxi_data, 'roamingTimeY2'); roamingTime_prepix = 'roamingTime-'
#
# regressionModel_dpath = '%s/%s' % (taxi_data, 'regressionModel'); regressionModel_prefix = 'regressionModel-'

# HOUR1 = 60 * 60
# causalityGraph_dpath = '%s/%s' % (taxi_data, 'causalityGraph'); causalityGraph_prefix = 'causalityGraph-'
#
#
#
#
#
#
#
# MIN_NUM_DRIVERS = 10



#



#
# rt_day_dir = '%s/%s' % (roaming_time_dir, 'day'); rt_day_prefix = 'roaming-time-day-'
# tf_zone_drivers_dir = '%s/%s' % (taxi_data, 'tf_zone_drivers'); tf_zone_drivers_prefix = 'tf-zone-drivers-'
# X_APPEAR, O_APPEAR = range(2)
# rt_appear_dir = '%s/%s' % (taxi_data, 'rt_appear'); rt_appear_prefix = 'rt-appear-'




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
