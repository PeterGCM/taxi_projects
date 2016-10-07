import community_analysis.a_detection
#
from taxi_common._classes import zone
from taxi_common._classes import driver
#
from community_analysis import THRESHOLD_VALUE, BY_COM_O, BY_COM_X


class ca_zone(zone):
    def __init__(self, boundary_relation_with_poly, gi, gj, cCoor_gps, polyPoints_gps):
        zone.__init__(self, boundary_relation_with_poly, gi, gj, cCoor_gps, polyPoints_gps)
        self.logQ = []

    def add_driver_in_logQ(self, t, d):
        self.logQ.append([t, d])

    def update_logQ(self, t):
        while self.logQ and self.logQ[0] < t - THRESHOLD_VALUE:
            self.logQ.pop(0)

    def init_logQ(self):
        self.logQ = []


class ca_driver(driver):
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
        #
        return None

    def init_linkage(self):
        self.linkage = {}
        self.num_pickup = 0


class ca_driver_with_com(ca_driver):
    def __init__(self, did, com_drivers):
        ca_driver.__init__(self, did)
        #
        for com_did in com_drivers:
            assert type(com_did) == type(did)
        self.com_drivers = com_drivers

    def update_linkage(self, t, z):
        z.update_logQ(t)
        updated_drivers = set()
        by_com = BY_COM_X
        for _, d in z.logQ:
            if d.did == self.did:
                continue
            if d.did in updated_drivers:
                continue
            else:
                updated_drivers.add(d.did)
                if d.did in self.com_drivers:
                    by_com = BY_COM_O
            if not self.linkage.has_key(d.did):
                self.linkage[d.did] = 0
            self.linkage[d.did] += 1
        z.add_driver_in_logQ(t, self)
        self.num_pickup += 1
        #
        return by_com

class ca_driver_with_com_prevD(ca_driver):
    def __init__(self, did, com_drivers):
        ca_driver.__init__(self, did)
        #
        for com_did in com_drivers:
            assert type(com_did) == type(did)
        self.com_drivers = com_drivers

    def update_linkage(self, t, z):
        z.update_logQ(t)
        updated_drivers = set()
        prevD = 'None'
        for _, d in z.logQ:
            if d.did == self.did:
                continue
            if d.did in updated_drivers:
                continue
            else:
                updated_drivers.add(d.did)
                if d.did in self.com_drivers:
                    prevD = d.did
            if not self.linkage.has_key(d.did):
                self.linkage[d.did] = 0
            self.linkage[d.did] += 1
        z.add_driver_in_logQ(t, self)
        self.num_pickup += 1
        #
        return prevD