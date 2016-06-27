from __init__ import singapore_poly_fn
#
from geo_functions import make_grid, generate_zones


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


def run(zone_unit_km, zone_class):
    singapore_poly_points, min_long, max_long, min_lat, max_lat = read_singapore_polygon()
    hl_unit, vl_unit, hl_points, vl_points = make_grid(zone_unit_km, min_long, max_long, min_lat, max_lat)
    zones = generate_zones(singapore_poly_points, hl_unit, hl_points, vl_unit, vl_points, zone_class)
    return hl_points, vl_points, zones
