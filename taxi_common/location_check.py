from __future__ import division
#
from shapely.geometry import Polygon, Point
from _setting import ap_poly_info, IN_AP, OUT_AP
from _setting import ns_poly_info, IN_NS, OUT_NS
#
class terminal_poly(Polygon):
    def __init__(self, tid, points):
        Polygon.__init__(self, points)
        self.tid = tid
    def __repr__(self):
        return self.tid

# generate airport's polygon and terminal polygones
ap_poly = None
term_polys = []
with open(ap_poly_info, 'r') as f:
    ls = [w.strip() for w in f.readlines()]
for l in ls:
    t, p = l.split('=')
    points = []
    for location in p[len('POLYGON(('):-len('))')].split(','):
        _long, _lat = location.split(' ')
        points.append([eval(_long), eval(_lat)])
    if t == 'Airport':
        ap_poly = Polygon(points)
    else:
        tn = eval(t.split('-')[1])
        term_polys.append(terminal_poly(tn, points))

# generate a polygon of night safari
ns_poly = None
with open(ns_poly_info, 'r') as f:
    ls = [w.strip() for w in f.readlines()]
points = []
for l in ls:
    _long, _lat = l.split(',')
    points.append([eval(_long), eval(_lat)])
ns_poly = Polygon(points)
#
def check_terminal_num(_long, _lat):
    '''
    tn: the terminal number
       if the location is not in polygons it will return -1
    '''
    p = Point(_long, _lat)
    tn = -1
    for poly in term_polys:
        if p.within(poly):
            tn = poly.tid
            break
    del p
    return tn

def is_in_night_safari(_long, _lat):
    '''
    if the location in night safari's polygon, return O
    otherwise, return X 
    '''
    p = Point(_long, _lat)
    rv = IN_NS if p.within(ns_poly) else OUT_NS
    del p
    return rv
    
def is_in_airport(_long, _lat):
    '''
    if the location in airport's polygon, return O
    otherwise, return X 
    '''
    p = Point(_long, _lat)
    rv = IN_AP if p.within(ap_poly) else OUT_AP
    del p
    return rv