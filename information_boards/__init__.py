import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/z_data'
try:
    check_dir_create(taxi_data)
except OSError:
    pass
#
# Trip mode define
#
ap_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '/src/airport_polygon'
ns_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '/src/night_safari_polygon'
DIn_PIn, DIn_POut, DOut_PIn, DOut_POut = range(4)
IN, OUT = True, False
#
AM2, AM5 = 2, 5
AM6 = 6
NUM, DUR, FARE = range(3)
# For meaningless data filtering
error_hours = [('9', '3', '15', '1'), ('10', '3', '17', '1'), ('10', '7', '4', '6'), ('10', '7', '4', '7'), ('10', '7', '4', '8'),
               # second filtering
                ('10', '3', '17', '6'), ('10', '11', '21', '6'), ('10', '11', '21', '10'),  # Abnormal (long) queueing time
                ('9', '3', '1', '1'), ('9', '11', '8', '1'), ('10', '5', '16', '1'), ('10', '1', '24', '1')  # Abnormal (short) active duration
               ]
# Singapore Public Holidays
HOLIDAYS2009 = [
            (2009,1,1),    # New Year's Day, Thursday, 1 January 2009
            (2009,1,26),    # Chinese New Year, Monday, 26 January 2009
            (2009,1,27),    # Chinese New Year, Tuesday, 27 January 2009
            (2009,4,10),    # Good Friday, Friday, 10 April 2009
            (2009,5,1),     # Labour Day, Friday, 1 May 2009
            (2009,5,9),     # Vesak Day, Saturday, 9 May 2009
            (2009,8,10),    # National Day, Sunday*, 9 August 2009
            (2009,9,21),    # Hari Raya Puasa, Sunday*, 20 September 2009
            (2009,11,16),   # Deepavali, Sunday*, 15 November 2009
            (2009,11,27),   # Hari Raya Haji, Friday, 27 November 2009
            (2009,12,25),   # Christmas Day, Friday, 25 December 2009
]
HOLIDAYS2010 = [(2010, 1, 1),  # New Year's Day, Friday, 1 January 2010
            (2010,2,16),  # Chinese New Year, Sunday*, 14 February 2010
            (2010,2,15),  # Chinese New Year, Monday, 15 February 2010
            (2010,4,2),  # Good Friday, Friday, 2 April 2010
            (2010,5,1),  # Labour Day, Saturday, 1 May 2010
            (2010,5,28),  # Vesak Day, Friday, 28 May 2010
            (2010,8,9),  # National Day, Monday, 9 August 2010
            (2010,9,10),  # Hari Raya Puasa, Friday, 10 September 2010
            (2010,11,5),  # Deepavali, Friday, 5 November 2010
            (2010,11,17),  # Hari Raya Haji, Wednesday, 17 November 2010
            (2010,11,17),  # Christmas Day, Saturday, 25 December 2010
                ]
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
WEEKENDS = [SAT, SUN]
#
ALL_DUR, ALL_FARE, ALL_NUM, \
AP_DUR, AP_FARE, AP_QUEUE, AP_NUM, \
NS_DUR, NS_FARE, NS_QUEUE, NS_NUM = range(11)
#
# directory path and file's prefix
#
dpaths, prefixs = {}, {}
dpaths['hourProductivity'] = '%s/%s' % (taxi_data, 'hourProductivity')
prefixs['hourProductivity'] = 'hourProductivity-'


trip_dpath, trip_prefix = '%s/%s' % (taxi_data, 'trip'), 'trip-'
trip_ap_dp_flow_prefix = 'trip-dp-flow-'
trip_ns_summary_fpath = '%s/trip-ns-summary.csv' % (trip_dpath)
#
crossingTime_dpath = '%s/%s' % (taxi_data, 'crossingTime')
crossingTime_ap_dpath, crossingTime_ap_prefix = '%s/%s' % (crossingTime_dpath, 'ap'), 'crossingTime-ap-'
crossingTime_ns_dpath, crossingTime_ns_prefix = '%s/%s' % (crossingTime_dpath, 'ns'), 'crossingTime-ns-'
log_dpath, log_prefix = '%s/%s' % (crossingTime_dpath, 'log'), 'log-'
log_last_day_dpath, log_last_day_prefix ='%s/%s' % (crossingTime_dpath, 'log_last_day'), 'log-last-day-'
#
queueingTime_dpath = '%s/%s' % (trip_dpath, 'queueingTime')
queueingTime_ap_dpath, queueingTime_ap_prefix = '%s/%s' % (queueingTime_dpath, 'ap'), 'trip-queueingTime-ap-'
queueingTime_ns_dpath, queueingTime_ns_prefix = '%s/%s' % (queueingTime_dpath, 'ns'), 'trip-queueingTime-ns-'
#
productivity_dpath, productivity_prefix = '%s/%s' % (taxi_data , 'productivity'), 'productivity-'
productivity_summary_fpath = '%s/productivity-summary.csv' % productivity_dpath
shift_dpath, shift_prefix = '/home/sfcheng/toolbox/results', 'shift-hour-state-'
shiftProDur_dpath, shiftProDur_prefix = '%s/%s' % (productivity_dpath, 'shiftProDur'), 'shiftProDur-'
#
economicProfit_dpath = '%s/%s' % (trip_dpath, 'economicProfit')
economicProfit_ap_dpath, economicProfit_ap_prefix = '%s/%s' % (economicProfit_dpath, 'ap'), 'trip-EP-ap-'
economicProfit_ns_dpath, economicProfit_ns_prefix = '%s/%s' % (economicProfit_dpath, 'ns'), 'trip-EP-ns-'
#
statistics_dpath= '%s/%s' % (taxi_data, 'statistics')
statisticsAllDrivers_dpath = '%s/%s' % (statistics_dpath, 'statisticsAllDrivers')
statisticsAllDrivers_ap_dpath = '%s/%s' % (statisticsAllDrivers_dpath, 'ap')
statisticsAllDriversDay_ap_prefix = 'statisticsAllDriversDay-ap-'
statisticsAllDriversMonth_ap_prefix = 'statisticsAllDriversMonth-ap-'
statisticsAllDriversYear_ap_prefix = 'statisticsAllDriversYear-ap-'
statisticsAllDriversTrip_ap_prefix = 'statisticsAllDriversTrip-ap-'
statisticsAllDriversIntellect_ap_prefix = 'statisticsAllDriversIntellect-ap-'

dpaths, prefixs = {}, {}
dpaths['individualAnalysis'] = '%s/%s' % (statisticsAllDrivers_ap_dpath, 'individualAnalysis')
prefixs['individualAnalysis'] = 'individualAnalysis-'



statisticsAllDrivers_ns_dpath = '%s/%s' % (statisticsAllDrivers_dpath, 'ns')
statisticsAllDriversTrip_ns1517_prefix = 'statisticsAllDriversTrip-ns1517-'
statisticsAllDriversDay_ns1517_prefix = 'statisticsAllDriversDay-ns1517-'
statisticsAllDriversMonth_ns1517_prefix = 'statisticsAllDriversMonth-ns1517-'
statisticsAllDriversYear_ns1517_prefix = 'statisticsAllDriversYear-ns1517-'
statisticsAllDriversTrip_ns2023_prefix = 'statisticsAllDriversTrip-ns2023-'
statisticsAllDriversDay_ns2023_prefix = 'statisticsAllDriversDay-ns2023-'
statisticsAllDriversMonth_ns2023_prefix = 'statisticsAllDriversMonth-ns2023-'
statisticsAllDriversYear_ns2023_prefix = 'statisticsAllDriversYear-ns2023-'


statisticsSsDrivers_dpath = '%s/%s' % (statistics_dpath, 'statisticsSsDrivers')
statisticsSsDrivers_ap_dpath = '%s/%s' % (statisticsSsDrivers_dpath, 'ap')
statisticsSsDriversDay_ap_prefix = 'statisticsSsDriversDay-ap-'
statisticsSsDriversMonth_ap_prefix = 'statisticsSsDriversMonth-ap-'
statisticsSsDriversTrip_ap_prefix = 'statisticsSsDriversTrip-ap-'
statisticsSsDrivers_ns_dpath = '%s/%s' % (statisticsSsDrivers_dpath, 'ns')

statisticsSsDriversDay_ns1517_prefix = 'statisticsSsDriversDay-ns1517-'
statisticsSsDriversMonth_ns1517_prefix = 'statisticsSsDriversMonth-ns1517-'
statisticsSsDriversTrip_ns1517_prefix = 'statisticsSsDriversTrip-ns1517-'

statisticsSsDriversDay_ns2023_prefix = 'statisticsSsDriversDay-ns2023-'
statisticsSsDriversMonth_ns2023_prefix = 'statisticsSsDriversMonth-ns2023-'
statisticsSsDriversTrip_ns2023_prefix = 'statisticsSsDriversTrip-ns2023-'




ssDriver_dpath = '%s/%s' % (taxi_data, 'ssDriver')
ssDriverTrip_dpath, ssDriverTrip_prefix = '%s/%s' % (ssDriver_dpath, 'ssDriverTrip'), 'ssDriverTrip-'
ssDriverShiftProDur_dpath, ssDriverShiftProDur_prefix = '%s/%s' % (ssDriver_dpath, 'ssDriverShiftProDur'), 'ssDriverShiftProDur-'
ssDriverEP_dpath = '%s/%s' % (ssDriver_dpath, 'ssDriverEP')
##
ssDriverEP_ap_dpath, ssDriverEP_ap_prefix = '%s/%s' % (ssDriverEP_dpath, 'ap'), 'ssDriverEP-ap-'
ssDriverEP_ap_all_fpath = '%s/ssDriverEP-ap-all.csv' % (ssDriverEP_ap_dpath)
ssDriversStatistics_ap_fpath = '%s/ssDriversStatisticsDayBased-ap.csv' % (ssDriverEP_ap_dpath)
ssDriversStatisticsDayBasedModi_ap_fpath = '%s/ssDriversStatisticsDayBasedModi-ap.csv' % (ssDriverEP_ap_dpath)
ssDriversStatisticsMonthBased2009_ap_fpath = '%s/ssDriversStatisticsMonthBased2009-ap.csv' % (ssDriverEP_ap_dpath)
ssDriversStatisticsMonthBased2010_ap_fpath = '%s/ssDriversStatisticsMonthBased2010-ap.csv' % (ssDriverEP_ap_dpath)


ssDriversStatisticsTripBased2009_ap_fpath = '%s/ssDriversStatisticsTripBased2009-ap.csv' % (ssDriverEP_ap_dpath)
ssDriversStatisticsTripBased2010_ap_fpath = '%s/ssDriversStatisticsTripBased2010-ap.csv' % (ssDriverEP_ap_dpath)

##
ssDriverEP_ns_dpath, ssDriverEP_ns_prefix = '%s/%s' % (ssDriverEP_dpath, 'ns'), 'ssDriverEP-ns-'
ssDriverEP_ns_all_fpath = '%s/ssDriverEP-ns-all.csv' % (ssDriverEP_ns_dpath)
ssDriversStatistics_ns1519_fpath = '%s/ssDriversStatisticsDayBased-ns1519.csv' % (ssDriverEP_ns_dpath)
ssDriversStatistics_ns2000_fpath = '%s/ssDriversStatisticsDayBased-ns2000.csv' % (ssDriverEP_ns_dpath)
ssDriversStatisticsDayBasedModi_ns1519_fpath = '%s/ssDriversStatisticsDayBasedModi-ns1519.csv' % (ssDriverEP_ns_dpath)
ssDriversStatisticsDayBasedModi_ns2000_fpath = '%s/ssDriversStatisticsDayBasedModi-ns2000.csv' % (ssDriverEP_ns_dpath)
ssDriversStatisticsMonthBased2009_ns1519_fpath = '%s/ssDriversStatisticsMonthBased2009-ns1519.csv' % (ssDriverEP_ns_dpath)
ssDriversStatisticsMonthBased2009_ns2000_fpath = '%s/ssDriversStatisticsMonthBased2009-ns2000.csv' % (ssDriverEP_ns_dpath)
ssDriversStatisticsMonthBased2010_ns1519_fpath = '%s/ssDriversStatisticsMonthBased2010-ns1519.csv' % (ssDriverEP_ns_dpath)
ssDriversStatisticsMonthBased2010_ns2000_fpath = '%s/ssDriversStatisticsMonthBased2010-ns2000.csv' % (ssDriverEP_ns_dpath)






##
#
arDriver_dpath = '%s/%s' % (taxi_data, 'arDriver')
arDriver2009_ap_fpath = '%s/aiDriver2009-ap.pkl' % (arDriver_dpath)
arDriver2010_ap_fpath = '%s/aiDriver2010-ap.pkl' % (arDriver_dpath)
arDriver2009_ns_fpath = '%s/aiDriver2009-ns.pkl' % (arDriver_dpath)
arDriver2010_ns_fpath = '%s/aiDriver2010-ns.pkl' % (arDriver_dpath)
arDriverTrip_dpath, arDriverTrip_prefix = '%s/%s' % (arDriver_dpath, 'arDriverTrip'), 'arDriverTrip-'
arDriverShiftProDur_dpath, arDriverShiftProDur_prefix = '%s/%s' % (arDriver_dpath, 'arDriverShiftProDur'), 'arDriverShiftProDur-'
arDriverEP_dpath = '%s/%s' % (arDriver_dpath, 'arDriverEP')
arDriverEP_ap_dpath, arDriverEP_ap_prefix = '%s/%s' % (arDriverEP_dpath, 'ap'), 'arDriverEP-ap-'
arDriverEP_ap_all_fpath = '%s/arDriverEP-ap-all.csv' % (arDriverEP_ap_dpath)
arDriverEP_ns_dpath, arDriverEP_ns_prefix = '%s/%s' % (arDriverEP_dpath, 'ns'), 'arDriverEP-ns-'
# Units
SEC3600, SEC600, SEC60 = 60 * 60.0, 10 * 60.0, 60.0
HOUR1 = SEC3600
CENT = 100.0
Q_LIMIT_MIN = 0
DAY_OF_WEEK = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
TIME_SLOTS = range(24)



