import __init__  # @UnusedImport

from taxi_common._classes import zone  # @UnresolvedImport
from taxi_common._classes import driver  # @UnresolvedImport
#
class rp_zone(zone):
    def __init__(self, relation_with_poly, i, j, x, y):
        zone.__init__(self, relation_with_poly, i, j, x, y)
        self.num_pickups, self.durations, self.scores = None, None, None
    def init_measures(self, num_timeslots):
        self.num_pickups, self.durations, self.scores = ([0] * num_timeslots for _ in xrange(3))
            
class rp_driver(driver):
    def __init__(self, did):
        driver.__init__(self, did)
        self.last_log_time, self.last_log_state = None, None
