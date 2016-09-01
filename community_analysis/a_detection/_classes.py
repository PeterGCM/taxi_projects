import __init__
#
from taxi_common._classes import zone  # @UnresolvedImport
from taxi_common._classes import driver  # @UnresolvedImport
#
from __init__ import THRESHOLD_VALUE


class cd_zone(zone):
    def __init__(self, boundary_relation_with_poly, gi, gj, x, y):
        zone.__init__(self, boundary_relation_with_poly, gi, gj, x, y)
        self.logQ = []

    def add_driver_in_logQ(self, t, d):
        self.logQ.append([t, d])

    def update_logQ(self, t):
        while self.logQ and self.logQ[0] < t - THRESHOLD_VALUE:
            self.logQ.pop(0)

    def init_logQ(self):
        self.logQ = []


class cd_driver(driver):
    def __init__(self, did):
        driver.__init__(self, did)
        self.linkage = {}
        self.num_pickup = 0

    def update_linkage(self, t, z):
        z.update_logQ(t)
        updated_drivers = set()
        for _, d in z.logQ:
            if d.did == self.did:
                continue
            if d.did in updated_drivers:
                continue
            else:
                updated_drivers.add(d.did)
            if not self.linkage.has_key(d.did):
                self.linkage[d.did] = 0
            self.linkage[d.did] += 1
        z.add_driver_in_logQ(t, self)
        self.num_pickup += 1

    def init_linkage(self):
        self.linkage = {}
        self.num_pickup = 0