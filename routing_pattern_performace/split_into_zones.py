from __init__ import singapore_poly_fn
#
from taxi_common._classes import zone #@UnresolvedImport
from taxi_common.geo_functions import make_grid, generate_zones #@UnresolvedImport
#
class rp_zone(zone):
    THRESHOLD_VALUE = None
    def __init__(self, relation_with_poly, i, j, x, y):
        zone.__init__(self, relation_with_poly, i, j, x, y)
        self.log_Q = []
    def add_driver_in_Q(self, t, d):
        self.log_Q.append([t, d])
    def update_Q(self, t):
        while self.log_Q and self.log_Q[0] < t - cd_zone.THRESHOLD_VALUE:
            self.log_Q.pop(0)

def read_singapore_polygon():
    #
    # Read Singapore polygon
    #  and return Polygon instance and min. max longitude and latitude
    #
    singapore_poly_points = []
    min_long, max_long, min_lat, max_lat = 1e400, -1e400, 1e400, -1e400
    #
    with open(singapore_poly_fn, 'r') as f:
        for l in f.readlines():
            _, _lat, _long = l.split(',')
            latitude, longitude = eval(_lat), eval(_long)
            min_lat, min_long = min(min_lat, latitude), min(min_long, longitude) 
            max_lat, max_long = max(max_lat, latitude), max(max_long, longitude)
            singapore_poly_points.append([longitude, latitude])
    #
    return singapore_poly_points, min_long, max_long, min_lat, max_lat

def run():
    singapore_poly_points, min_long, max_long, min_lat, max_lat = read_singapore_polygon()
    hl_unit, vl_unit, hl_points, vl_points = make_grid(min_long, max_long, min_lat, max_lat)
    zones = generate_zones(singapore_poly_points, hl_unit, hl_points, vl_unit, vl_points, rp_zone)
    return hl_points, vl_points, zones
