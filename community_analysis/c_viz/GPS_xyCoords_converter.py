import __init__
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, save_pickle_file
from taxi_common.geo_functions import get_SG_polygon, get_SG_roads
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
