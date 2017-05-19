import __init__
#
from taxi_common import sg_maps_dpath
import geopandas as gpd
from taxi_common import sg_loc_polygons_fpath
from file_handling_functions import check_path_exist, load_pickle_file, save_pickle_file
from _classes import zone
#
from pykml import parser
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
                       "id": '%d#%d' % (i,j),
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


def get_ap_polygons():
    poly_names = ['T1', 'T2', 'T3', 'BudgetT']
    kml_doc = None
    with open(sg_loc_polygons_fpath) as f:
        kml_doc = parser.parse(f).getroot().Document
    ap_polygons = []
    for pm in kml_doc.Placemark:
        if pm.name in poly_names:
            str_coords = str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates)
            points = []
            for l in ''.join(str_coords.split()).split(',0')[:-1]:
                _long, _lat = l.split(',')
                points.append([eval(_long), eval(_lat)])
            ap_poly = poly(points)
            ap_poly.name = pm.name
            ap_polygons.append(ap_poly)
    return ap_polygons


def get_ns_polygon():
    kml_doc = None
    with open(sg_loc_polygons_fpath) as f:
        kml_doc = parser.parse(f).getroot().Document
    for pm in kml_doc.Placemark:
        if pm.name == 'Night Safari':
            str_coords = str(pm.Polygon.outerBoundaryIs.LinearRing.coordinates)
            points = []
            for l in ''.join(str_coords.split()).split(',0')[:-1]:
                _long, _lat = l.split(',')
                points.append([eval(_long), eval(_lat)])
            return poly(points)


def get_SG_polygon():
    ifpath = '%s/%s' % (sg_maps_dpath, 'singapore_admin.geojson')
    ofpath = '%s/%s' % (sg_maps_dpath, 'sg_border.pkl')
    if check_path_exist(ofpath):
        sg_border = load_pickle_file(ofpath)
        return sg_border
    df = gpd.read_file(ifpath)
    sg_border = list(df.ix[0].geometry.exterior.coords)
    save_pickle_file(ofpath, sg_border)
    return sg_border

def get_SG_roads():
    ofpath = '%s/%s' % (sg_maps_dpath, 'sg_roads.pkl')
    if check_path_exist(ofpath):
        roads = load_pickle_file(ofpath)
        return roads
    sg_border = Polygon(get_SG_polygon())
    ifpath = '%s/%s' % (sg_maps_dpath, 'singapore_roads.geojson')
    df = gpd.read_file(ifpath)
    roads = []
    for r, n in df.loc[:, ('geometry', 'name')].values:
        if r.within(sg_border):
            roads += [(n, list(r.coords))]
    save_pickle_file(ofpath, roads)
    return roads


if __name__ == '__main__':
    get_SG_roads()
    # print get_SG_polygon()
    # get_ns_polygon()
    # ap_polygons = get_ap_polygons()
    # target_gps = (103.984857,  1.342390)
    # for ap_poly in ap_polygons:
    #     if ap_poly.is_including(target_gps):
    #         print ap_poly.name


