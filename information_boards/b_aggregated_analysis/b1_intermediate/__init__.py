import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
from b_aggregated_analysis import __init__
#
GEN_DUR, GEN_FARE, AP_DUR, AP_FARE, AP_QUEUE, NS_DUR, NS_FARE, NS_QUEUE = range(8)