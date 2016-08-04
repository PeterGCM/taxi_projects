import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'
check_dir_create(taxi_data)
#
logs_dir = taxi_data + '/logs'
ld_dir = taxi_data + '/linkage_daily'
lm_dir = taxi_data + '/linkage_monthly'
la_dir = taxi_data + '/linkage_annually'
pg_dir = taxi_data + '/partitioned_group'
for _dir in [logs_dir, ld_dir, lm_dir, la_dir, pg_dir]:
    check_dir_create(_dir)
#
FREE, POB = 0, 5
THRESHOLD_VALUE = 30 * 60
MIN_LINKAGE_NUM, MIN_LINKAGE_RATIO, REMAINING_LINKAGE_RATIO = 2, 0.2, 0.9
ONE_HOUR, SIX_HOUR, EIGHT_HOUR, HOUR12, HOUR24 = 1, 6, 8, 12, 24
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
PM2, PM3 = 14, 15