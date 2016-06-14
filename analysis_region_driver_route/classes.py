from __future__ import division

IN, INTERSECT, OUT = range(3)

class zone(object):
    x_unit, y_unit = None, None
    def __init__(self, relation_with_poly, x, y):
        self.relation_with_poly = relation_with_poly
        self.x, self.y = x, y
        self.log_Q = []
    def check_validation(self):
        if self.relation_with_poly == IN or self.relation_with_poly == INTERSECT:
            return True
        else:
            return False
    
#         [x, y],
#      [x + x_unit, y],
#      [x + x_unit, y + y_unit],
#      [x, y + y_unit]]


class driver(object):
    def __init__(self, did):
        self.did = did
        self.current_zone = None