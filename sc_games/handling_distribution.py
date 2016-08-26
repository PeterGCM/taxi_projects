from bisect import bisect
from random import random


def choose_index_wDist(distribution):
    cdf = [distribution[0]]
    for i in xrange(1, len(distribution)):
        cdf.append(cdf[-1] + distribution[i])
    return bisect(cdf, random())


if __name__ == '__main__':
    distribution = [0.10, 0.25, 0.60, 0.05]
    for i in xrange(20):
        print choose_index_wDist(distribution)