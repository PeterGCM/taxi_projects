from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
from a_overall_analysis import __init__
#
IN, OUT = True, False
#
ap_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '../../src/airport_polygon'
ns_poly_fn = os.path.dirname(os.path.realpath(__file__)) + '../../src/night_safari_polygon'