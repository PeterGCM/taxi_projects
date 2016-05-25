from __future__ import division
#
from shapely.geometry import Polygon, Point, LineString
from math import ceil
from geopy.distance import vincenty

M_TO_KM = 1000

with open('Singapore_polygon', 'r') as f:
    ls = [w.strip() for w in f.readlines()]
singapore_poly_points = []
min_lat, max_lat, min_long, max_long = 1e400, -1e400, 1e400, -1e400


for l in ls:
    _, _lat, _long = l.split(',')
    num_float = len(_long[_long.index('.'):])
    latitude, longitude = eval(_lat), eval(_long)
    min_lat, min_long = min(min_lat, latitude), min(min_long, longitude) 
    max_lat, max_long = max(max_lat, latitude), max(max_long, longitude)
    singapore_poly_points.append([longitude * 10 ** (num_float - 1), latitude * 10 ** (num_float - 1)])
singapore_poly = Polygon(singapore_poly_points)
#
western_end, eastern_end = (min_long, (min_lat + max_lat) / 2), (max_long, (min_lat + max_lat) / 2) 
southern_end, northern_end = ((min_lat + max_lat) / 2, min_lat), ((min_lat + max_lat) / 2, max_lat)

singapore_width_km = (vincenty(western_end, eastern_end).meters) / M_TO_KM
singapore_height_km = (vincenty(southern_end, northern_end).meters) / M_TO_KM
num_cols, num_rows = int(ceil(singapore_width_km)), int(ceil(singapore_height_km)) 
num_width_lines, num_height_lines = num_cols - 1, num_rows - 1

x0, y0 = min_long, min_lat 
vertical_lines, horizontal_lines = [], []
# modi with intersection points

for x1 in [round(x0 + (i + 1) * (max_long - min_long) / singapore_width_km, 6) for i in xrange(num_width_lines)]:
    sx, sy = x1 * 10 ** (num_float - 1), min_lat * 10 ** (num_float - 1)
    ex, ey = x1 * 10 ** (num_float - 1), max_lat * 10 ** (num_float - 1)
    shapely_line = LineString([(sx, sy), (ex, ey)])
    l_str = str(singapore_poly.intersection(shapely_line))
    if l_str.startswith('LINESTRING'):
        (new_sx, new_sy), (new_ex, new_ey) = list(singapore_poly.intersection(shapely_line).coords) 
        vertical_lines.append([new_sx, new_sy, new_ex, new_ey])
    else:
        assert l_str.startswith('MULTILINESTRING')
        for l in singapore_poly.intersection(shapely_line):
            (new_sx, new_sy), (new_ex, new_ey) = list(l.coords) 
            vertical_lines.append([new_sx, new_sy, new_ex, new_ey])

for y1 in [round(y0 + (i + 1) * (max_lat - min_lat) / singapore_height_km, 6) for i in xrange(num_height_lines)]:
    sx, sy = min_long * 10 ** (num_float - 1), y1 * 10 ** (num_float - 1)
    ex, ey = max_long * 10 ** (num_float - 1), y1 * 10 ** (num_float - 1)
    shapely_line = LineString([(sx, sy), (ex, ey)])
    l_str = str(singapore_poly.intersection(shapely_line))
    if l_str.startswith('LINESTRING'):
        (new_sx, new_sy), (new_ex, new_ey) = list(singapore_poly.intersection(shapely_line).coords) 
        horizontal_lines.append([new_sx, new_sy, new_ex, new_ey])
    else:
        assert l_str.startswith('MULTILINESTRING')
        for l in singapore_poly.intersection(shapely_line):
            (new_sx, new_sy), (new_ex, new_ey) = list(l.coords) 
            horizontal_lines.append([new_sx, new_sy, new_ex, new_ey])

