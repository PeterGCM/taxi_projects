from __future__ import division
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../..')
import stochastic_congestion_games.__init__

MOVING, WAITING, POB, IDLE = range(4)
Prob_SHOW = 0.8
ALPH, GAMMA = 0.5, 0.08
ONE_SIGMA = 1
EPSILON = 0.0000001