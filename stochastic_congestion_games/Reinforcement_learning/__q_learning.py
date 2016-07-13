import __init__
from __init__ import ALPH, GAMMA


def simple_q_learning(Q_sa, s0, a, s1, reward):
    Q_sa[s][a] += ALPH * (reward + GAMMA * max(Q_sa[a]) - Q_sa[s][a])