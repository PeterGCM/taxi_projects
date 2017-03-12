import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/z_data';
try:
    check_dir_create(taxi_data)
except OSError:
    pass
shift_dpath, shift_prefix = '/home/sfcheng/toolbox/results', 'shift-hour-state-'
dpaths, prefixs = {}, {}
for irName in ['roamingNinterTravel', 'prevDrivers']:
    dpaths[irName] = '%s/%s' % (taxi_data, irName)
    prefixs[irName] = '%s-' % irName
for depVar in ['roamingTime', 'interTravelTime']:
    for irName in ['priorPresence', 'influenceGraph', 'graphPartition',
                   'comTrips']:
        dpaths[depVar, irName] = '%s/%s/%s' % (taxi_data, depVar, irName)
        prefixs[depVar, irName] = '%s-%s-' % (depVar, irName)


#
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
AM10, PM8 = 10, 20
MINUTES40 = 40 * 60
HISTORY_LOOKUP_LENGTH = 30 * 60
FREE, POB = 0, 5
MIN20 = 20 * 60.0
X_PRESENCE, O_PRESENCE = range(2)
#
SIGINIFICANCE_LEVEL = 0.05
# SIGINIFICANCE_LEVEL = 0.01
MIN_PICKUP_RATIO = 0.1
MIN_RATIO_RESIDUAL = 0.2
#






# chart_dpath = os.path.dirname(os.path.realpath(__file__)) + '/chart'; check_dir_create(chart_dpath)
# years = ['20%02d' % y for y in range(9, 13)]
# ss_trips_dpath, ss_trips_prefix = '%s/%s' % (taxi_data, 'trips_ss_drivers'), 'trips-ss-drivers-'
# shiftProDur_dpath, shiftProDur_prefix = '%s/%s' % (taxi_data, 'shiftProDur'), 'shiftProDur-'
#
# prevDriversDefined_dpath, prevDriversDefined_prefix =  '%s/%s' % (taxi_data, 'prevDriversDefined'), 'prevDriversDefined-'
# tfZ_TP_dpath, tfZ_TP_prefix = '%s/%s' % (taxi_data, 'tfZ_TP'), 'tfZ_TP-'
# driversRelations_fpaths = {year: '%s/driversRelations%s.pkl' % (prevDriversDefined_dpath, year) for year in years}
# #
# timeMeasures = ['spendingTime', 'roamingTime']
# interResults = ['influenceGraph',
#                 'groupPartition', 'groupTrips', 'groupShifts','groupZones', 'groupMarginal',
#                 'groupDriverStats','groupDayStats',
#                 'groupEvolution', 'groupAttributes']
# dpaths, prefixs = {}, {}
# for tm in timeMeasures:
#     for year in years:
#         for ir in interResults:
#             dpaths[tm, year, ir] = '%s/%s/%s/%s' % (taxi_data, tm, year, ir)
#             prefixs[tm, year, ir] = '%s-%s-%s-' % (tm, year, ir)
#
# groupPartitionSummaries, groupPartitionDrivers = {}, {}
# for tm in timeMeasures:
#     for year in years:
#         groupPartition_dpath = dpaths[tm, year, 'groupPartition']
#         groupPartition_prefix = prefixs[tm, year, 'groupPartition']
#         groupPartitionSummaries[tm, year] = '%s/%s' % (groupPartition_dpath, groupPartition_prefix)
# groupEvolution_fpath = '%s/%s/%s' % (taxi_data, 'spendingTime', 'groupEvolution.csv')
# #
#
# interResults = ['countGraph',
#                 'groupPartition', 'groupTrips', 'groupShifts','groupZones', 'groupMarginal',
#                 'groupDriverStats','groupDayStats']
# for ir in interResults:
#     dpaths['baseline', '2009', ir] = '%s/%s/%s/%s' % (taxi_data, 'baseline', '2009', ir)
#     prefixs['baseline', '2009', ir] = '%s-%s-%s-' % ('baseline', '2009', ir)
