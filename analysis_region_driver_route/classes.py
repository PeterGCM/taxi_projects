from __future__ import division

IN, INTERSECT, OUT = range(3)

THRESHOLD_VALUE = 60 * 15

class zone(object):
    x_unit, y_unit = None, None
    def __init__(self, relation_with_poly, i, j, x, y):
        self.relation_with_poly = relation_with_poly
        self.i, self.j = i, j
        self.x, self.y = x, y
        self.log_Q = []
        self.num_visit, self.num_pickup = 0, 0
        
#         [x, y],
#      [x + x_unit, y],
#      [x + x_unit, y + y_unit],
#      [x, y + y_unit]]

    def __repr__(self):
        return 'zone (%d,%d)' % (self.i, self.j)
    def check_validation(self):
        if self.relation_with_poly == IN or self.relation_with_poly == INTERSECT:
            pass
        else:
            # Originally there should be now log in this zone
            # But because I manually draw a polygon of Singpaore, there can be error
            self.relation_with_poly = INTERSECT
    def add_driver_in_Q(self, t, d):
        self.num_visit += 1
        self.log_Q.append([t, d])
    def update_Q(self, t):
        self.num_pickup += 1
        while self.log_Q and self.log_Q[0] < t - THRESHOLD_VALUE:
            self.log_Q.pop(0)

class driver(object):
    def __init__(self, did):
        self.did = did
        self.current_zone = None
        self.relation = {}
    def __repr__(self):
        return 'did %s' % str(self.did)
    def update_position(self, t, z):
        if self.current_zone != z:
            self.current_zone = z
            self.current_zone.add_driver_in_Q(t, self)
    def update_relation(self, z):
        for _, d in z.log_Q:
            if self == d:
                continue
            if not self.relation.has_key(d.did):
                self.relation[d.did] = 0
            self.relation[d.did] += 1
