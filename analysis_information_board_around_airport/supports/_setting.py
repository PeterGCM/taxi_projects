from __future__ import division

import platform, sys

# Check environments and set a prefix for finding files and libraries
plf = platform.platform()
if plf.startswith('Linux'):
    # This would be the server
    prefix = '/home/ckhan/taxi_data'
    py_vinfo = sys.version_info
    if py_vinfo.major == 2 and py_vinfo.minor == 7:
        sys.path.append('/home/ckhan/local/lib/python2.7/site-packages')
        sys.path.append('/home/ckhan/local/lib64/python2.7/site-packages')
    else:
        print 'This python is not 2.7 version'
        assert False
    #
elif plf.startswith('Darwin'):
    # This is my Macbook Pro
    prefix = '/Users/JerryHan88/taxi_data'
else:
    # TODO
#     assert False, 'Windows?'
    prefix = 'C:\Users/ckhan.2015/taxi_data'
assert prefix
#
# trips(_merged)
#
merged_trip_dir = prefix + '/trips_merged'
trips_dir, trip_prefix = prefix + '/trips', 'whole-trip-'
airport_trips_dir, ap_trip_prefix = trips_dir + '/airport_trips', 'airport-trip-'
nightsafari_trips_dir, ns_trip_prefix = trips_dir + '/nightsafari_trips', 'nightsafari-trip-'
#
# logs
#
logs_dir = prefix + '/logs'
log_last_day_dir = logs_dir + '/logs_last_day'
#
# shifts
#
shifts_dir, shifts_prefix = prefix + '/shifts', 'shift-hour-state-'
shift_pro_dur_dir, shift_pro_dur_prefix = shifts_dir + '/shift_pro_dur', 'shift-pro-dur-'
#
# hourly_productivities
#
hourly_productivities_dir = prefix + '/hourly_productivities'
general_dur_fare_dir, general_dur_fare_prefix = hourly_productivities_dir + '/general_dur_fare', 'gdf-'
ap_dur_fare_q_time_dir, ap_dur_fare_q_time_prefix = hourly_productivities_dir + '/ap_dur_fare_q_time', 'adfqt-'
ns_dur_fare_q_time_dir, ns_dur_fare_q_time_prefix = hourly_productivities_dir + '/ns_dur_fare_q_time', 'ndfqt-'
#
# ap_trips_economic_profits_dir
#
ap_trips_economic_profits_dir = prefix + '/ap_trips_economic_profits'
ap_trips_ecoprof_prefix = 'ap-trip-ecoprof-'
#
# ns_trips_economic_profits_dir
#
ns_trips_economic_profits_dir = prefix + '/ns_trips_economic_profits'
ns_trips_ecoprof_prefix = 'ns-trip-ecoprof-'
#
# summary
#
summary_dir = prefix + '/summary'
ap_tm_num_dur_fare_fn = summary_dir +'/ap-tm-num-dur-fare.csv' 
ns_tm_num_dur_fare_fn = summary_dir +'/ns-tm-num-dur-fare.csv'
hourly_productivities = summary_dir + '/hourly-productivities.csv'
zero_duration_time_slots = summary_dir + '/zero-duration-time-slots.pkl'
Y09_ap_trips = summary_dir + '/Y09-ap-trips.csv'
Y10_ap_trips = summary_dir + '/Y10-ap-trips.csv'
Y09_ns_trips = summary_dir + '/Y09-ns-trips.csv'
Y10_ns_trips = summary_dir + '/Y10-ns-trips.csv'
driver_monthly_fare_gt = summary_dir + '/driver-monthly-fare-gt.pkl'
driver_monthly_fare_at = summary_dir + '/driver-monthly-fare-at.pkl'
driver_monthly_fare_nt = summary_dir + '/driver-monthly-fare-nt.pkl'
#

full_shift_dir = shifts_dir + '/full_time_drivers' 





for_learning_dir = prefix + '/for_learning'
for_full_driver_dir = prefix + '/full_drivers_trips_q_comparision'

 


hourly_summary = trips_dir + '/hourly_summary'


#
# For Q-learning
#
DAY_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TIME_SLOTS = range(24)



individual_dir = prefix + '/individual-summary'
individual_detail_dir = prefix + '/individual-detail-summary'


#
ap_poly_info = '../_src/airport_polygons'
IN_AP, OUT_AP = 'O', 'X'
ns_poly_info = '../_src/night_safari_polygon'
IN_NS, OUT_NS = 'O', 'X'
#
# trip modes
#
DInAP_PInAP, DInAP_POutAP, DOutAP_PInAP, DOutAP_POutAP = range(4)
DInNS_PInNS, DInNS_POutNS, DOutNS_PInNS, DOutNS_POutNS = range(4)
#
# units
#
HOUR, MINUTE = 60 * 60, 60
CENT = 100
#
#
#
Q_LIMIT_MIN, Q_LIMIT_MAX = 0, HOUR * 3
MAX_DURATION = HOUR 
PROD_LIMIT = 65 / HOUR * CENT
#
# Labeling for zero duration
#
GENERAL, AIRPORT, NIGHTSAFARI = 'G', 'A', 'N'
#
TIME_ALARM = MINUTE * 5