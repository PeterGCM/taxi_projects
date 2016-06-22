from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
for p in sys.path:
    print p
#
from a_overall_analysis import __init__
#
IN, OUT = True, False
#
ap_poly_fn, ns_poly_fn = '../src/airport_polygon', '../src/night_safari_polygon'