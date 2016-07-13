import __init__
#
from __init__ import singapore_poly_fn, singapore_grid_xy_points, singapore_zones
from __init__ import ZONE_UNIT_KM
#
from geo_functions import make_grid, generate_zones
from file_handling_functions import check_path_exist, save_pickle_file, load_pickle_file


def generate_singapore_grid():
    #
    # Read Singapore polygon
    #  and return Polygon instance and min. max longitude and latitude
    #
    min_long, max_long, min_lat, max_lat = 1e400, -1e400, 1e400, -1e400
    #
    with open(singapore_poly_fn, 'r') as f:
        for l in f.readlines():
            _, _lat, _long = l.split(',')
            latitude, longitude = eval(_lat), eval(_long)
            min_lat, min_long = min(min_lat, latitude), min(min_long, longitude) 
            max_lat, max_long = max(max_lat, latitude), max(max_long, longitude)
    #
    hl_unit, vl_unit, x_points, y_points = make_grid(ZONE_UNIT_KM, min_long, max_long, min_lat, max_lat)
    return hl_unit, vl_unit, x_points, y_points


def get_singapore_poly_points():
    singapore_poly_points = []
    with open(singapore_poly_fn, 'r') as f:
        for l in f.readlines():
            _, _lat, _long = l.split(',')
            latitude, longitude = eval(_lat), eval(_long)
            singapore_poly_points.append([longitude, latitude])
    return singapore_poly_points


def get_singapore_zones():
    if not check_path_exist(singapore_zones):
        if not check_path_exist(singapore_grid_xy_points):
            hl_unit, vl_unit, x_points, y_points = generate_singapore_grid()
        else:
            hl_unit, vl_unit, x_points, y_points = load_pickle_file(singapore_grid_xy_points)
        zones = generate_zones(get_singapore_poly_points(), hl_unit, vl_unit, x_points, y_points)
        save_pickle_file(singapore_zones, zones)
    else:
        zones = load_pickle_file(singapore_zones)
    return zones


def get_singapore_grid_xy_points():
    if not check_path_exist(singapore_grid_xy_points):
        hl_unit, vl_unit, x_points, y_points = generate_singapore_grid()
        save_pickle_file(singapore_grid_xy_points, [hl_unit, vl_unit, x_points, y_points])
    else:
        _, _, x_points, y_points = load_pickle_file(singapore_grid_xy_points)
    return x_points, y_points


