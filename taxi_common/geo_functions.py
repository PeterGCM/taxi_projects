from __future__ import division
#
from math import ceil
from shapely.geometry import Polygon, LineString, Point
from geopy.distance import vincenty
#
from classes import zone
#
METER1000 = 1000

def make_grid(min_long, max_long, min_lat, max_lat, consider_visualization=False):
    western_end, eastern_end = (min_long, (min_lat + max_lat) / 2), (max_long, (min_lat + max_lat) / 2) 
    southern_end, northern_end = ((min_lat + max_lat) / 2, min_lat), ((min_lat + max_lat) / 2, max_lat)
    hl_length, vl_length = max_long - min_long, max_lat - min_lat
    #
    width_km = (vincenty(western_end, eastern_end).meters) / METER1000
    height_km = (vincenty(southern_end, northern_end).meters) / METER1000
    hl_unit, vl_unit = hl_length / width_km, vl_length / height_km
    #
    num_cols, num_rows = int(ceil(width_km)), int(ceil(height_km))
    #
    hl_points = [min_long + i * hl_unit for i in xrange(num_cols)]
    vl_points = [min_lat + j * vl_unit for j in xrange(num_rows)]
    #
    if consider_visualization:
        return hl_unit, vl_unit, hl_points, vl_points, hl_length, vl_length
    else:
        return hl_unit, vl_unit, hl_points, vl_points

def generate_zones(poly_points, x_unit, x_points, y_unit, y_points, zone_class):
    poly = Polygon(poly_points)
    zones = {}
    for i, x in enumerate(x_points):
        for j, y in enumerate(y_points):
            zone_poly = Polygon([[x, y],
                                 [x + x_unit, y],
                                 [x + x_unit, y + y_unit],
                                 [x, y + y_unit]]
                                )
            if poly.contains(zone_poly):
                relation = zone.IN 
            elif poly.intersects(zone_poly):
                relation = zone.INTERSECT
            else:
                relation = zone.OUT
            zones[(i, j)] = zone_class(relation, i, j, x, y)
    return zones

class poly(Polygon):
    def __init__(self, poly_points):
        Polygon.__init__(self, poly_points)
    def is_including(self, coordinate):
        assert type(coordinate) == type(tuple) and len(coordinate) == 2
        p = Point(*coordinate)
        return p.within(self)
