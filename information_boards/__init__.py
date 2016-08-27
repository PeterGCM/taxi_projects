import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data_20160826'
check_dir_create(taxi_data)
# Trip mode
DIn_PIn, DIn_POut, DOut_PIn, DOut_POut = range(4)
IN, OUT = True, False
# Units
SEC3600, SEC60 = 60 * 60, 60
CENT = 100
Q_LIMIT_MIN = 0
#
DAY_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TIME_SLOTS = range(24)
# summary and charts directory
summary_dir = taxi_data + '/summary'
charts_dir = taxi_data + '/charts'
tables_dir = taxi_data + '/tables'
check_dir_create(summary_dir); check_dir_create(charts_dir); check_dir_create(tables_dir)
#
from taxi_common.geo_functions import read_generate_polygon
ap_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '/src/airport_polygon'
ns_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '/src/night_safari_polygon'
ap_poly, ns_poly = read_generate_polygon(ap_poly_fn), read_generate_polygon(ns_poly_fn)
# For meaningless data_20160826 filtering
AM2, AM5 = 2, 5
error_period = [('9', '3', '15', '1'), ('10', '3', '17', '1'), ('10', '7', '4', '6'), ('10', '7', '4', '7'), ('10', '7', '4', '8')]