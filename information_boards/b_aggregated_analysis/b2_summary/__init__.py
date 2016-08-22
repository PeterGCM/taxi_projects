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
GEN_DUR, GEN_FARE, \
AP_DUR, AP_FARE, AP_QUEUE, \
NS_DUR, NS_FARE, NS_QUEUE = range(8)