import __init__
#
from __init__ import IDLE, MOVING, POB
#
from taxi_common.classes import driver
#
from random import randrange, normalvariate, shuffle
import numpy as np
#
ONE_SIGMA = 1
ALPH, GAMMA = 0.8, 0.6
EPSILON = 0.0000001

def run(num_agents, num_zones, time_horizon, fl, Re, Co, d0, problem_saving_dir):
    # Generate drivers and initialize their location
    zones = [scg_zone(i) for i in xrange(num_zones)]
    drivers = []
    num_count, i = 0, 0
    for did in xrange(num_agents):
        drivers.append(scg_driver(did, zones[i]))
        num_count += 1
        if num_count == d0[i]:
            num_count = 0
            i += 1
    #
    dist_ranking = []
    for l1 in [[np.mean(l2) for l2 in zip(*l1)] for l1 in zip(*Co)]:
        l2 = []
        for i, v in enumerate(l1):
            l2.append([v, i])
        l2.sort()
        dist_ranking.append([i for _, i in l2])
    #
    Q_sa = [[0] * num_zones for _ in xrange(num_zones)]
    num_iter = 0
    count_Q = 0
    while True:
        for z in zones:
                z.passengers = []
        # drivers state and Q-value update
        Q_value_changing = False
        for d in [d for d in drivers if d.state != IDLE]:
            d.time_to_arrival -= 1
            if d.time_to_arrival == 0:
                Q_value_changing = True
                if d.state == POB:
                    reward = d.revenue - d.cost
                    d.revenue, d.cost = 0, 0
                else:
                    assert d.state == MOVING
                    reward = -d.cost
                    d.cost = 0
                Q_sa[d.from_zone.zid][d.to_zone.zid] += ALPH * \
                                    (reward + GAMMA * max(Q_sa[d.from_zone.zid]) - Q_sa[d.from_zone.zid][d.to_zone.zid])
                count_Q += 1
                d.to_zone.add_driver(d)
                d.from_zone = d.to_zone; d.to_zone = None
                d.state = IDLE

        if num_iter != 0 and Q_value_changing:
            print num_iter, count_Q, Q_sa
            # pi1 = [np.argmax(Q_sa[i]) for i in xrange(len(Q_sa))]
            # for i in xrange(len(pi0)):
            #     if pi0[i] != pi1[i]:
            #         break
            # else:
            #     break
            Q_sa1 = [x[:] for x in Q_sa]
            diff = False
            for i in xrange(len(Q_sa0)):
                for j in xrange(len(Q_sa0[i])):
                    if abs(Q_sa0[i][j] - Q_sa1[i][j]) < EPSILON:
                        continue
                    else:
                        diff = True
                        break
                if diff:
                    break
            else:
                break
        #
        pi0 = [np.argmax(Q_sa[i]) for i in xrange(len(Q_sa))]
        Q_sa0 = [x[:] for x in Q_sa]
        #
        # t = randrange(time_horizon)
        t = 1
        # Apply policy
        for d in [d for d in drivers if d.state == IDLE]:
            next_z_id = pi0[d.from_zone.zid]
            if d.from_zone.zid != next_z_id:
                d.to_zone = zones[next_z_id]
                d.time_to_arrival = dist_ranking[d.from_zone.zid].index(d.to_zone.zid) + 1
                d.cost = Co[t][d.from_zone.zid][d.to_zone.zid]
                d.state = MOVING
                #
                d.from_zone.remove_driver(d)

        # Passenger generation
        passengers = [[int(normalvariate(fl[t][i][j], ONE_SIGMA))
                       for j in xrange(len(fl[t][i]))] for i in xrange(len(fl[t]))]
        for src, zone_passenger in enumerate(passengers):
            for dest, num_passenger in enumerate(zone_passenger):
                for _ in xrange(num_passenger):
                    zones[src].add_passenger([dest, Re[t][src][dest], Co[t][src][dest]])
        # Passenger boarding
        for z in zones:
            departuring_drivers = []
            for d in z.drivers.itervalues():
                z.passengers.sort()
                if len(z.passengers) > 0:
                    dest, revenue, cost = z.passengers.pop()
                    #
                    d.to_zone = zones[dest]
                    d.time_to_arrival = dist_ranking[d.from_zone.zid].index(d.to_zone.zid) + 1
                    d.revenue, d.cost = revenue, cost
                    d.state = POB
                    #
                    departuring_drivers.append(d)
            for d in departuring_drivers:
                d.from_zone.remove_driver(d)
        if Q_value_changing:
            num_iter += 1
    print pi0


class scg_zone(object):
    def __init__(self, zid):
        self.zid = zid
        self.drivers, self.passengers = {}, []

    def __repr__(self):
        return str(self.zid)

    def add_driver(self, d):
        self.drivers[d.did]= d
        d.cur_z = self

    def remove_driver(self, d):
        self.drivers.pop(d.did)

    def add_passenger(self, p):
        self.passengers.append(p)


class scg_driver(driver):
    def __init__(self, did, z):
        driver.__init__(self, did)
        self.from_zone, self.to_zone = z, None
        self.time_to_arrival = 0
        self.revenue, self.cost = 0, 0
        self.state = IDLE
        #
        self.from_zone.add_driver(self)

    def __repr__(self):
        return '(did:%s, %s, %s-%s)' % (str(self.did), str(self.state), str(self.from_zone), str(self.to_zone))


if __name__ == '__main__':
    from problems import p1
    from problems import p2
    run(*p1())