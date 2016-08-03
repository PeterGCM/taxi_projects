import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import community_analysis.__init__
#
FREE, POB = 0, 5
MON, TUE, WED, THR, FRI, SAT, SUN = range(7)
PM2, PM3 = 14, 15
MIN_DAILY_LINKAGE = 2
MIN_MONTHLY_LINKAGE = 2
#
THRESHOLD_VALUE = 30 * 60