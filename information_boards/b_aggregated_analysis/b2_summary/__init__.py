from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
from b_aggregated_analysis import __init__
#
# Labeling for zero duration
#
ALL, AP, AP_GEN, NS, NS_GEN = 'A', 'AP', 'AP_GEN', 'NS', 'NS_GEN'
#
ALL_DUR, ALL_FARE, ALL_NUM, \
AP_DUR, AP_FARE, AP_QUEUE, AP_NUM, \
NS_DUR, NS_FARE, NS_QUEUE, NS_NUM = range(11)