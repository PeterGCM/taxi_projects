from __future__ import division

#
fl, Re, Co = None, None, None


#

def define_DDAP(_fl, _Re, _Co):
    global fl, Re, Co
    fl, Re, Co = _fl, _Re, _Co
    return _PHI, _R


def _R(t, s0, a, d):
    if sum(fl[t][s0]) >= d[s0]:
        # C1
        reward = sum(_PHI(t, d, s0, a, s1) * (Re[t][s0][s1] - Co[t][s0][s1]) for s1 in xrange(len(d)))
    else:
        reward = 0
        for s1 in xrange(len(d)):
            if a != s1:
                # C2
                reward += _PHI(t, d, s0, a, s1) * (Re[t][s0][s1] - Co[t][s0][s1])
            elif a == s1:
                # C3
                reward += (fl[t][s0][s1] / d[s0]) * Re[t][s0][s1] - _PHI(t, d, s0, a, s1) * Co[t][s0][s1]
            else:
                assert False
    return reward


def _PHI(t, d, s0, a, s1):
    if sum(fl[t][s0]) >= d[s0]:
        # C1
        return fl[t][s0][s1] / sum(fl[t][s0])
    elif a != s1 and sum(fl[t][s0]) < d[s0]:
        # C2
        return fl[t][s0][s1] / d[s0]
    elif a == s1 and sum(fl[t][s0]) < d[s0]:
        # C3
        return 1 - (sum([fl[t][s0][s1] for s in xrange(len(d)) if s != s1]) / d[s0])


if __name__ == '__main__':
    pass