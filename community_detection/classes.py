from __init__ import THRESHOLD_VALUE

from taxi_common.classes import zone  # @UnresolvedImport
from taxi_common.classes import driver  # @UnresolvedImport
#
class cd_zone(zone):
    def __init__(self, relation_with_poly, i, j, x, y):
        zone.__init__(self, relation_with_poly, i, j, x, y)
        self.log_Q = []
    def add_driver_in_Q(self, t, d):
        self.log_Q.append([t, d])
    def update_Q(self, t):
        while self.log_Q and self.log_Q[0] < t - THRESHOLD_VALUE:
            self.log_Q.pop(0)
            
class cd_driver(driver):
    def __init__(self, did):
        driver.__init__(self, did)
        self.current_zone = None
        self.relation = {}
    def update_position(self, t, z):
        if self.current_zone != z:
            self.current_zone = z
            self.current_zone.add_driver_in_Q(t, self)
    def update_relation(self, t, z):
        z.update_Q(t)
        for _, d in z.log_Q:
            if self == d:
                continue
            if not self.relation.has_key(d.did):
                self.relation[d.did] = 0
            self.relation[d.did] += 1
