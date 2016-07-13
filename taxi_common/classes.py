import __init__


class zone(object):
    IN, INTERSECT, OUT = range(3)

    def __init__(self, relation_with_poly, i, j, x, y):
        self.relation_with_poly = relation_with_poly
        self.loc_grid = (i, j)
        self.x, self.y = x, y

    def __repr__(self):
        return 'zone %s' % str(self.loc_grid)

    def check_validation(self):
        if self.relation_with_poly == zone.IN or self.relation_with_poly == zone.INTERSECT:
            return True
        else:
            # Originally there should be now log in this zone
            # But because I manually draw a polygon of Singpaore, there can be error
            return False


class driver(object):
    def __init__(self, did):
        self.did = did

    def __repr__(self):
        return 'did %s' % str(self.did)