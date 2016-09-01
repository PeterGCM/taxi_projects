import __init__
#
from __init__ import sg_poly_fpath, sg_grid_xy_points, sg_zones
from __init__ import ZONE_UNIT_KM
#
from geo_functions import make_grid, generate_zones
from file_handling_functions import check_path_exist, save_pickle_file, load_pickle_file


def generate_sg_grid():
    #
    # Read Singapore polygon
    #  and return Polygon instance and min. max longitude and latitude
    #
    min_long, max_long, min_lat, max_lat = 1e400, -1e400, 1e400, -1e400
    #
    with open(sg_poly_fpath, 'r') as f:
        for l in f.readlines():
            _, _lat, _long = l.split(',')
            latitude, longitude = eval(_lat), eval(_long)
            min_lat, min_long = min(min_lat, latitude), min(min_long, longitude) 
            max_lat, max_long = max(max_lat, latitude), max(max_long, longitude)
    #
    x_points, y_points = make_grid(ZONE_UNIT_KM, min_long, max_long, min_lat, max_lat)
    return x_points, y_points


def get_sg_poly_points():
    singapore_poly_points = []
    with open(sg_poly_fpath, 'r') as f:
        for l in f.readlines():
            _, _lat, _long = l.split(',')
            latitude, longitude = eval(_lat), eval(_long)
            singapore_poly_points.append([longitude, latitude])
    return singapore_poly_points


def get_sg_zones():
    if not check_path_exist(sg_zones):
        if not check_path_exist(sg_grid_xy_points):
            x_points, y_points = generate_sg_grid()
        else:
            x_points, y_points = load_pickle_file(sg_grid_xy_points)
        xaxis_unit, yaxis_unit = x_points[1] - x_points[0], y_points[1] - y_points[0]
        zones = generate_zones(get_sg_poly_points(), xaxis_unit, yaxis_unit, x_points, y_points)
        save_pickle_file(sg_zones, zones)
    else:
        zones = load_pickle_file(sg_zones)
    return zones


def get_sg_grid_xy_points():
    if not check_path_exist(sg_grid_xy_points):
        x_points, y_points = generate_sg_grid()
        save_pickle_file(sg_grid_xy_points, [x_points, y_points])
    else:
        x_points, y_points = load_pickle_file(sg_grid_xy_points)
    return x_points, y_points


if __name__ == '__main__':
    print get_sg_zones()
