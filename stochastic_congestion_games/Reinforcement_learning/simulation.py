import __init__
#
from __init__ import MOVING, WAITING, POB, IDLE
from __init__ import ONE_SIGMA, EPSILON
from q_learning import simple_q_learning
#
from taxi_common.classes import driver
#
from random import randrange, normalvariate, shuffle, sample
from heapq import heappush, heappop
import numpy as np
#
zones, drivers = {}, []
fl, Re, Co, Mt = None, None, None, None
#
event_queue = []
now = 0.0
current_event = None


def push_event(t, handler, args=()):
    e = [t, handler, args]
    heappush(current_event)
    return e


def take_action(d):
    global zones
    pi = [np.argmax(d.Q_sa[i]) for i in xrange(len(d.Q_sa))]
    zfrom = d.zone_from
    zto = zones[pi[zfrom.zid]]
    time_to_arrival = Mt[zfrom.zid][zto.zid]
    cost = Co[zfrom.zid][zto.zid]
    #
    d.veh_state = MOVING
    zfrom.remove_driver(d)
    d.zone_to = zto
    d.moving_cost = cost
    push_event(now + time_to_arrival, finish_moving, d)


def check_convergence(Q_sa0, Q_sa1):
    convergence, diff = False, False
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
        convergence = True
    return convergence


def finish_moving(d):
    zfrom = d.zone_from
    zto = d.zone_from
    cost = d.moving_cost
    Q_sa0 = [x[:] for x in d.Q_sa]
    simple_q_learning(d.Q_sa, zfrom.zid, zto.zid, -cost)
    d.Q_convergence = check_convergence(Q_sa0, d.Q_sa)
    #
    d.veh_state = WAITING
    zto.add_driver(d)
    d.zone_from, d.zone_to = zto, None
    d.moving_cost = 0.0

def display_results():
    pass

def on_passenger_arrival(args=None):
    global drivers, zones, event_queue
    # Check driver's Q_convergence
    if len(drivers) == len([d for d in driver if d.Q_convergence]):
        # End simulation
        display_results()
        event_queue = []
    else:
        for zfrom in zones:
            passengers = []
            for zto in zones:
                num_passengers = int(normalvariate(fl[zfrom.zid][zto.zid], ONE_SIGMA))
                for _ in xrange(num_passengers):
                    passengers.append(zto)
            shuffle(passengers)
            waiting_drivers = [d for d in zfrom.drivers if d.veh_state == WAITING]
            if len(passengers) < len(waiting_drivers):
                driver_get_hired = sample(waiting_drivers, len(passengers))
            else:
                driver_get_hired = waiting_drivers
            for i, d in enumerate(driver_get_hired):
                zfrom = zones[d.zone_from.zid]
                zdest = passengers[i]
                time_to_arrival = Mt[zfrom.zid][zdest.zid]
                cost = Co[zfrom.zid][zdest.zid]
                revenue = Re[zfrom.zid][zdest.zid]
                #
                d.veh_state = POB
                zfrom.remove_driver(d)
                d.zone_to = zdest
                d.moving_cost = cost
                d.service_revenue = revenue
                push_event(now + time_to_arrival, finish_service, d)


def finish_service(d):
    zfrom = d.zone_from
    zto = d.zone_from
    revenue, cost = d.service_revenue, d.moving_cost
    Q_sa0 = [x[:] for x in d.Q_sa]
    simple_q_learning(d.Q_sa, zfrom.zid, zto.zid, revenue - cost)
    d.Q_convergence = check_convergence(Q_sa0, d.Q_sa)
    #
    d.veh_state = IDLE
    zto.add_driver(d)
    d.zone_from, d.zone_to = zto, None
    d.service_revenue, d.moving_cost = 0.0, 0.0
    #
    take_action(d)


def run(num_agents, num_zones, time_horizon, _fl, _Re, _Co, _Mt, d0, problem_saving_dir):
    for x in [_fl, _Re, _Co, _Mt]:
        assert len(x) == time_horizon
    global fl, Re, Co, Mt
    fl, Re, Co, Mt = _fl[0], _Re[0], _Co[0], _Mt[0]
    #
    driver_count = 0
    for i, num in enumerate(d0):
        z = scg_zone(i)
        zones[z.zid] = z
        for _ in xrange(num):
            d = scg_driver(driver_count, range(num_zones), range(num_zones), z)
            drivers.append(d)
            z.add_driver(d)
            driver_count += 1
            #
            push_event(now, take_action, d)
    assert num_agents == driver_count
    push_event(now, on_passenger_arrival, None)
    #
    global now, current_event
    num_iter = 0
    while event_queue:
        current_event = heappop(event_queue)
        evt_time, hdlr, args = current_event
        now = evt_time
        hdlr(*args)


class scg_zone(object):
    def __init__(self, zid):
        self.zid = zid
        self.drivers, self.passengers = {}, []

    def __repr__(self):
        return 'zid %d' % (self.zid)

    def add_driver(self, d):
        self.drivers[d.did]= d
        d.cur_z = self

    def remove_driver(self, d):
        self.drivers.pop(d.did)


class scg_driver(driver):
    def __init__(self, did, states, actions, z):
        driver.__init__(self, did)
        self.Q_sa = {}
        for s in states:
            for a in actions:
                self.Q_sa[s, a] = 0.0
        self.Q_convergence = False
        self.zone_from, self.zone_to = z, None
        self.service_revenue, self.moving_cost = 0.0, 0.0
        self.veh_state = IDLE

    def __repr__(self):
        return '(did %d, %s, %s -> %s)' % (self.did, str(self.veh_state), str(self.from_zone), str(self.to_zone))



if __name__ == '__main__':
    # from problems import p1
    # from problems import p2
    from problems import p0
    run(*p0())