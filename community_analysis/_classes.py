from community_analysis import THRESHOLD_VALUE
from community_analysis import DEPRECIATION_LAMBDA

from taxi_common._classes import zone
from taxi_common._classes import driver
#
import datetime


class ca_zone(zone):
    def __init__(self, boundary_relation_with_poly, zi, zj, cCoor_gps, polyPoints_gps):
        zone.__init__(self, boundary_relation_with_poly, zi, zj, cCoor_gps, polyPoints_gps)
        self.logQ = []

    def add_driver_in_logQ(self, t, d):
        self.logQ.append([t, d])

    def update_logQ(self, t):
        while self.logQ and self.logQ[0] < t - THRESHOLD_VALUE:
            self.logQ.pop(0)

    def init_logQ(self):
        self.logQ = []


class ca_driver_with_distribution(driver):
    def __init__(self, did, individual_distribution, group_distribution):
        driver.__init__(self, did)
        self.individual_distribution = individual_distribution
        self.group_distribution = group_distribution
        self.num_inDay = {}
        self.link_weight, self.link_frequency = {}, {}
        self.num_pickup = 0

    def update_linkWeight(self, t, z):
        z.update_logQ(t)
        updated_drivers = set()
        for _, driverPrev in z.logQ:
            if driverPrev == self:
                continue
            if driverPrev in updated_drivers:
                continue
            else:
                updated_drivers.add(driverPrev)
            if not self.link_weight.has_key(driverPrev.did):
                self.num_inDay[driverPrev.did] = 0
                self.link_weight[driverPrev.did] = 0.0
                self.link_frequency[driverPrev.did] = 0.0
            cur_dt = datetime.datetime.fromtimestamp(t)
            k = (cur_dt.hour, z.zi, z.zj)
            curD_prob = self.individual_distribution[k]
            if not driverPrev.group_distribution.has_key(k):
                prevD_group_prob = 0.0
            else:
                prevD_group_prob = driverPrev.group_distribution[k]
            self.link_weight[driverPrev.did] += max(0, prevD_group_prob - curD_prob) * self.link_frequency[driverPrev.did]
            self.num_inDay[driverPrev.did] += 1
        z.add_driver_in_logQ(t, self)
        self.num_pickup += 1

    def update_linkFrequency(self):
        for prev_did in self.link_frequency.iterkeys():
            self.link_frequency[prev_did] = DEPRECIATION_LAMBDA * self.link_frequency[prev_did] + self.num_inDay[prev_did]
        #
        for prev_did in self.num_inDay.iterkeys():
            self.num_inDay[prev_did] = 0


class ca_driver_with_com_prevD(driver):
    def __init__(self, did, com_drivers):
        driver.__init__(self, did)
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
        z.add_driver_in_logQ(t, self)
        #
        return prevD