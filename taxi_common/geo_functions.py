import __init__
#
from __init__ import METER1000
from classes import zone
#
from math import ceil
from shapely.geometry import Polygon, Point
from geopy.distance import vincenty


def make_grid(zone_unit_km, min_long, max_long, min_lat, max_lat, consider_visualization=False):
    western_end, eastern_end = (min_long, (min_lat + max_lat) / float(2)), (max_long, (min_lat + max_lat) / float(2))
    southern_end, northern_end = ((min_lat + max_lat) / float(2), min_lat), ((min_lat + max_lat) / float(2), max_lat)
    hl_length, vl_length = max_long - min_long, max_lat - min_lat
    #
    width_km = (vincenty(western_end, eastern_end).meters) / float(METER1000) * zone_unit_km
    height_km = (vincenty(southern_end, northern_end).meters) / float(METER1000) * zone_unit_km
    hl_unit, vl_unit = hl_length / float(width_km), vl_length / float(height_km)
    #
    num_cols, num_rows = int(ceil(width_km)), int(ceil(height_km))
    #
    x_points = [min_long + i * hl_unit for i in xrange(num_cols)]
    y_points = [min_lat + j * vl_unit for j in xrange(num_rows)]
    #
    if consider_visualization:
        return hl_unit, vl_unit, x_points, y_points, hl_length, vl_length
    else:
        return hl_unit, vl_unit, x_points, y_points


def generate_zones(poly_points, hl_unit, vl_unit, x_points, y_points):
    poly = Polygon(poly_points)
    zones = {}
    for i, x in enumerate(x_points):
        for j, y in enumerate(y_points):
            zone_poly = Polygon([[x, y],
                                 [x + hl_unit, y],
                                 [x + hl_unit, y + vl_unit],
                                 [x, y + vl_unit]]
                                )
            if poly.contains(zone_poly):
                relation = zone.IN 
            elif poly.intersects(zone_poly):
                relation = zone.INTERSECT
            else:
                relation = zone.OUT
            zones[(i, j)] = zone(relation, i, j, x, y)
    return zones


class poly(Polygon):
    def __init__(self, poly_points):
        Polygon.__init__(self, poly_points)

    def is_including(self, coordinate):
        assert type(coordinate) == type(()), coordinate 
        assert len(coordinate) == 2, len(coordinate) 
        p = Point(*coordinate)
        return p.within(self)


def read_generate_polygon(fn):
    with open(fn, 'r') as f:
        ls = [w.strip() for w in f.readlines()]
    points = []
    for l in ls:
        _long, _lat = l.split(',')
        points.append([eval(_long), eval(_lat)])
    return poly(points)