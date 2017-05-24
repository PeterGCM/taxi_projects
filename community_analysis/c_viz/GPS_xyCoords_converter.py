import __init__
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, save_pickle_file
from taxi_common.geo_functions import get_SG_polygon, get_SG_roads
from taxi_common.sg_grid_zone import generate_sg_grid
from taxi_common.sg_grid_zone import get_sg_zones
#
scale = 2500
min_lon, max_lon = 1e400, -1e400
min_lat, max_lat = 1e400, -1e400
#
sg_border = get_SG_polygon()
for lon, lat in sg_border:
    if lon < min_lon:
        min_lon = lon
    if lon > max_lon:
        max_lon = lon
    if lat < min_lat:
        min_lat = lat
    if lat > max_lat:
        max_lat = lat


def convert_GPS2xy(lon, lat):
    x = (lon - min_lon) * scale
    y = (max_lat - (lat - min_lat)) * scale
    return x, y


def get_sgBoarder_xy():
    fpath = 'sgBorder_xy.pkl'
    if not check_path_exist(fpath):
        sgBorder_xy = []
        for lon, lat in sg_border:
            x, y = convert_GPS2xy(lon, lat)
            sgBorder_xy += [(x, y)]
        save_pickle_file(fpath, sgBorder_xy)
    else:
        sgBorder_xy = load_pickle_file(fpath)
    return sgBorder_xy


def get_sgRoards_xy():
    ofpath = 'sgRoards_xy.pkl'
    if check_path_exist(ofpath):
        sgRoards_xy = load_pickle_file(ofpath)
    else:
        sgRoards_xy = []
        for _, coords in get_SG_roads():
            road_fd = []
            for lon, lat in coords:
                road_fd += [convert_GPS2xy(lon, lat)]
            sgRoards_xy += [road_fd]
        save_pickle_file(ofpath, sgRoards_xy)
    return sgRoards_xy


def get_sgGrid_xy():
    ofpath = 'sgGrid_xy.pkl'
    if check_path_exist(ofpath):
        sgGrid_xy = load_pickle_file(ofpath)
    else:
        sgGrid_xy = []
        lons, lats = generate_sg_grid()
        for lon in lons:
            sx, sy = convert_GPS2xy(lon, lats[0])
            ex, ey = convert_GPS2xy(lon, lats[-1])
            sgGrid_xy += [[(sx, sy), (ex, ey)]]
        for lat in lats:
            sx, sy = convert_GPS2xy(lons[0], lat)
            ex, ey = convert_GPS2xy(lons[-1], lat)
            sgGrid_xy += [[(sx, sy), (ex, ey)]]
        save_pickle_file(ofpath, sgGrid_xy)
    return sgGrid_xy


def get_sgZones():
    ofpath = 'sgZone.pkl'
    if check_path_exist(ofpath):
        sgZones = load_pickle_file(ofpath)
    else:
        sgZones = get_sg_zones()
        for z in sgZones.values():
            z.cCoor_xy = convert_GPS2xy(*z.cCoor_gps)
            z.polyPoints_xy = [convert_GPS2xy(*gps_coord) for gps_coord in z.polyPoints_gps]
            z.marked = False
        save_pickle_file(ofpath, sgZones)
    return sgZones


if __name__ == '__main__':
    print get_sgZones()
