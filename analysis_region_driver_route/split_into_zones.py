from __future__ import division
#
from _setting import singapore_poly_fn
from _setting import METER1000
from classes import zone, IN, INTERSECT, OUT
#
from shapely.geometry import Polygon, LineString
from geopy.distance import vincenty
from math import ceil

def run():
    singapore_poly_points, min_long, max_long, min_lat, max_lat = read_singapore_polygon()
    #
    x_unit, x_length, x_points, y_unit, y_length, y_points = make_grid(min_long, max_long, min_lat, max_lat)
    #
    zones = generate_zones(singapore_poly_points, x_unit, x_points, y_unit, y_points)
    #
    lines = generate_lines_for_visualization(singapore_poly_points, x_unit, x_length, x_points, y_unit, y_length, y_points)
    #
    return x_points, y_points, zones, singapore_poly_points, lines

def generate_lines_for_visualization(singapore_poly_points, x_unit, x_length, x_points, y_unit, y_length, y_points):
    def add_lines(sx, sy, ex, ey):
        shapely_line = LineString([(sx, sy), (ex, ey)])
        l_str = str(singapore_poly.intersection(shapely_line))
        if l_str.startswith('LINESTRING'):
            (new_sx, new_sy), (new_ex, new_ey) = list(singapore_poly.intersection(shapely_line).coords) 
            lines.append([new_sx, new_sy, new_ex, new_ey])
        elif l_str.startswith('MULTILINESTRING'):
            for l in singapore_poly.intersection(shapely_line):
                (new_sx, new_sy), (new_ex, new_ey) = list(l.coords) 
                lines.append([new_sx, new_sy, new_ex, new_ey])
        else:
            assert l_str.startswith('POINT')
    #
    singapore_poly = Polygon(singapore_poly_points)
    lines = []
    # Vertical lines
    for x in x_points:
        sx, sy = x, y_points[0]
        ex, ey = x, y_points[0] + y_length
        add_lines(sx, sy, ex, ey)
    # Horizontal lines
    for y in y_points:
        sx, sy = x_points[0], y 
        ex, ey = x_points[0] + x_length, y
        add_lines(sx, sy, ex, ey)
    #
    return lines
    
def generate_zones(singapore_poly_points, x_unit, x_points, y_unit, y_points):
    singapore_poly = Polygon(singapore_poly_points)
    zones = {}
    zone.x_unit, zone.y_unit = x_unit, y_unit
    for i, x in enumerate(x_points):
        for j, y in enumerate(y_points):
            zone_poly = Polygon([[x, y],
                                 [x + x_unit, y],
                                 [x + x_unit, y + y_unit],
                                 [x, y + y_unit]]
                                )
            if singapore_poly.contains(zone_poly):
                z = zone(IN, x, y) 
            elif singapore_poly.intersects(zone_poly):
                z = zone(INTERSECT, x, y) 
            else:
                z = zone(OUT, x, y)
            zones[(i, j)] = z
    return zones

def make_grid(min_long, max_long, min_lat, max_lat):
    western_end, eastern_end = (min_long, (min_lat + max_lat) / 2), (max_long, (min_lat + max_lat) / 2) 
    southern_end, northern_end = ((min_lat + max_lat) / 2, min_lat), ((min_lat + max_lat) / 2, max_lat)
    x_length, y_length = max_long - min_long, max_lat - min_lat
    #
    width_km = (vincenty(western_end, eastern_end).meters) / METER1000
    height_km = (vincenty(southern_end, northern_end).meters) / METER1000
    x_unit, y_unit = x_length / width_km, y_length / height_km
    #
    num_cols, num_rows = int(ceil(width_km)), int(ceil(height_km))
    #
    x_points = [min_long + i * x_unit for i in xrange(num_cols)]
    y_points = [min_lat + j * y_unit for j in xrange(num_rows)]
    #
    return x_unit, x_length, x_points, y_unit, y_length, y_points   
    
def read_singapore_polygon():
    #
    # Read Singapore polygon
    #  and return Polygon instance and min. max logitude and latitude
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

if __name__ == '__main__':
    run()
