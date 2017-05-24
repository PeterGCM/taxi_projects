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
for irName in ['roamingNinterTravel', 'prevDrivers', 'driverLog', 'driverTrip']:
    dpaths[irName] = '%s/%s' % (taxi_data, irName)
    prefixs[irName] = '%s-' % irName
for depVar in ['roamingTime', 'interTravelTime']:
    for irName in ['priorPresence', 'sigRelation',
                   'individual',
                   'influenceGraph', 'graphPartition',
                   'comTrips', 'comEvolution']:
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
# SIGINIFICANCE_LEVEL = 0.05
SIGINIFICANCE_LEVEL = 0.01
MIN_PICKUP_RATIO = 0.1
MIN_RATIO_RESIDUAL = 0.2
#