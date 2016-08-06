import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'; check_dir_create(taxi_data)
charts_dir = taxi_data + '/charts'; check_dir_create(charts_dir)
#
logs_dir = taxi_data + '/logs'; check_dir_create(logs_dir)
ld_dir = taxi_data + '/linkage_daily'; check_dir_create(ld_dir)
lm_dir = taxi_data + '/linkage_monthly'; check_dir_create(lm_dir)
la_dir = taxi_data + '/linkage_annually'; check_dir_create(la_dir)
pg_dir = taxi_data + '/partitioned_group'; check_dir_create(pg_dir)
#
trips_dir = taxi_data + '/trips'; check_dir_create(trips_dir)
#
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
PM2, PM3 = 14, 15