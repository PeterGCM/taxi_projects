import __init__
#
from _classes import zone
#
from math import ceil
from shapely.geometry import Polygon, Point
from geopy.distance import vincenty, VincentyDistance
#
NORTH, EAST, SHOUTH, WEST = 0, 90, 180, 270
METER1000 = 1000


def make_grid(zone_unit_km, min_long, max_long, min_lat, max_lat, consider_visualization=False):
    W_end_gps, E_end_gps = (min_long, (min_lat + max_lat) / float(2)), (max_long, (min_lat + max_lat) / float(2))
    S_end_gps, N_end_gps = ((min_lat + max_lat) / float(2), min_lat), ((min_lat + max_lat) / float(2), max_lat)
    width_km = (vincenty(W_end_gps, E_end_gps).meters) / float(METER1000)
    height_km = (vincenty(S_end_gps, N_end_gps).meters) / float(METER1000)
    num_cols, num_rows = map(int, map(ceil, [v / float(zone_unit_km) for v in [height_km, width_km]]))
    #
    hl_length_gps, vl_length_gps = max_long - min_long, max_lat - min_lat


    xaxis_unit, yaxis_unit = hl_length_gps / float(num_cols), vl_length_gps / float(num_rows)
    x_points = [min_long + i * xaxis_unit for i in xrange(num_cols)]
    y_points = [min_lat + j * yaxis_unit for j in xrange(num_rows)]

    p0, p1 = (y_points[0], x_points[0]), (y_points[0], x_points[1])
    x_dist = (vincenty(p0, p1).meters) / float(METER1000)

    p0, p1 = (y_points[0], x_points[0]), (y_points[1], x_points[0])
    y_dist = (vincenty(p0, p1).meters) / float(METER1000)

    d = VincentyDistance(kilometers=zone_unit_km)


    print p0, d.destination(point=p0, bearing=0).latitude, d.destination(point=p0, bearing=0).longitude


    # print x_dist, y_dist, len(x_points), len(y_points)


    assert False

    return xaxis_unit, yaxis_unit, x_points, y_points
    # assert False
    #
    # xaxis_unit, yaxis_unit = hl_length_gps / float(width_km), vl_length_gps / float(height_km)
    # #
    # num_cols, num_rows = int(ceil(width_km)), int(ceil(height_km))
    # #
    # x_points = [min_long + i * xaxis_unit for i in xrange(num_cols)]
    # y_points = [min_lat + j * yaxis_unit for j in xrange(num_rows)]
    # #
    # if consider_visualization:
    #     return xaxis_unit, yaxis_unit, x_points, y_points, hl_length_gps, vl_length_gps
    # else:
    #     return xaxis_unit, yaxis_unit, x_points, y_points


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