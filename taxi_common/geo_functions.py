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


def make_grid(zone_unit_km, min_long, max_long, min_lat, max_lat):
    mover = VincentyDistance(kilometers=zone_unit_km)
    x = min_long
    x_points = []
    while x < max_long:
        x_points.append(x)
        #
        p0 = [min_lat, x]
        moved_point = mover.destination(point=p0, bearing=EAST)
        x = moved_point.longitude
    y = min_lat
    y_points = []
    while y < max_lat:
        y_points.append(y)
        #
        p0 = [y, min_long]
        moved_point = mover.destination(point=p0, bearing=NORTH)
        y = moved_point.latitude
    return x_points, y_points


def generate_zones(poly_points, xaxis_unit, yaxis_unit, x_points, y_points):
    poly = Polygon(poly_points)
    zones = {}
    geo_json = {"type": "FeatureCollection", "features": []}
    for i, x in enumerate(x_points):
        for j, y in enumerate(y_points):
            leftBottom, rightBottom = (x, y), (x + xaxis_unit, y)
            rightTop, leftTop = (x + xaxis_unit, y + yaxis_unit), (x, y + yaxis_unit)
            polyPoints_gps = [leftBottom, rightBottom, rightTop, leftTop, leftBottom]
            cCoor_gps = (y + yaxis_unit / float(2), x + xaxis_unit / float(2))
            zone_poly = Polygon(polyPoints_gps)
            if poly.contains(zone_poly):
                boundary_relation = zone.IN
            elif poly.intersects(zone_poly):
                boundary_relation = zone.INTERSECT
            else:
                boundary_relation = zone.OUT
            zones[(i, j)] = zone(boundary_relation, i, j, cCoor_gps, polyPoints_gps)
            feature = {"type":"Feature",
                       "id": 'z%03d%03d' % (i,j),
                       "properties": {"cCoor_gps": cCoor_gps},
                       "geometry":
                           {"type": "Polygon",
                            "coordinates": [[leftBottom,
                                            rightBottom,
                                            rightTop,
                                            leftTop,
                                            leftBottom
                                            ]]
                            }
                      }
            geo_json["features"].append(feature)
    return zones, geo_json


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