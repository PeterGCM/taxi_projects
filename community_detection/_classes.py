import __init__
#
from taxi_common.classes import zone  # @UnresolvedImport
from taxi_common.classes import driver  # @UnresolvedImport
#
from __init__ import THRESHOLD_VALUE


class cd_zone(zone):
    def __init__(self, relation_with_poly, i, j, x, y):
        zone.__init__(self, relation_with_poly, i, j, x, y)
        self.logQ = []

    def add_driver_in_logQ(self, t, d):
        self.logQ.append([t, d])

    def update_logQ(self, t):
        while self.logQ and self.logQ[0] < t - THRESHOLD_VALUE:
            self.logQ.pop(0)


class cd_driver(driver):
    def __init__(self, did):
        driver.__init__(self, did)
        self.linkage = {}

    def update_linkage(self, t, z):
        z.update_logQ(t)
        for _, d in z.logQ:
            if not self.linkage.has_key(d.did):
                self.linkage[d.did] = 0
            self.linkage[d.did] += 1
        z.add_driver_in_logQ(t, self)
