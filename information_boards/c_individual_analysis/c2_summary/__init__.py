from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
#
from c_individual_analysis import __init__
#
import pandas as pd
#
from c_individual_analysis.__init__ import Y09_ftd_gen_stat, Y10_ftd_gen_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat
from c_individual_analysis.__init__ import Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat

_package = [Y09_ftd_gen_stat, Y10_ftd_gen_stat,
            Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat,
            Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat,
            Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat,
            Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat]
dfs = [pd.read_csv(path_fn) for path_fn in _package]
#
Y09_GEN, Y10_GEN, \
Y09_PIAP, Y10_PIAP, \
Y09_POAP, Y10_POAP, \
Y09_PINS, Y10_PINS, \
Y09_PONS, Y10_PONS = range(10)