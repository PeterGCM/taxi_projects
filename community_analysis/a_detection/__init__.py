import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import community_analysis.__init__
#
FREE, POB = 0, 5
MIN_DAILY_LINKAGE, MIN_MONTHLY_LINKAGE = 2, 2
REMAINING_LINKAGE_RATIO = 0.5
#
THRESHOLD_VALUE = 30 * 60