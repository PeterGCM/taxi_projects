from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import stochastic_congestion_games.__init__

policy_prefix, x_prefix, dist_prefix, lp_prefix = 'policy-', 'x-', 'dist-', 'LP-MODEL-'