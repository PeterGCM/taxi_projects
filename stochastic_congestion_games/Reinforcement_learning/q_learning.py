import __init__
#
from __init__ import MOVING, WAITING, POB, IDLE
from __init__ import EPSILON
from __init__ import Prob_SHOW
from __init__ import ALPH, GAMMA
from simulation import push_event, process_events, finish_simulation
#
from random import shuffle, sample
import numpy as np
#
zones, agents = {}, []
P, S, A, fl, Re, Co, Mt = None, None, None, None, None, None
#
num_demand_generation = 0


def run(num_agents, num_zones, time_horizon, _fl, _Re, _Co, _Mt, d0, problem_saving_dir):
    for x in [_fl, _Re, _Co, _Mt]:
        assert len(x) == time_horizon
    global P, S, A, fl, Re, Co, Mt
    P, S, A, fl, Re, Co, Mt = range(num_agents), range(num_zones), range(num_zones), _fl[0], _Re[0], _Co[0], _Mt[0]
    #
    count_agent = 0
    for i, num in enumerate(d0):
        z = scg_zone(i)
        zones[z.zid] = z
        for _ in xrange(num):
            agent = scg_agent(count_agent, z)
            agents.append(agent)
            z.add_agent(agent)
            count_agent += 1
            #
            push_event(0, take_action, agent)
    assert num_agents == count_agent
    push_event(0, on_demand_arrival, None)
    #
    process_events()


def take_action(agt):
    max_Q_value, max_a = -1e400, None
    for a in A:
        Q_sa_value = agt.Q_sa[agt.s0, a]
        if max_Q_value < Q_sa_value:
            max_Q_value = Q_sa_value
            max_a = a
    #
    agt.sim_state = MOVING
    zones[agt.s0].remove_agent(agt)
    agt.a = max_a
    agt.cost = Co[agt.s0][agt.a]
    #
    push_event(Mt[agt.s0][agt.a], finish_action, agt)


def finish_action(agt):
    agt.sim_state = WAITING
    zones[agt.a].add_agent(agt)


def on_demand_arrival(_):
    global num_demand_generation
    num_demand_generation += 1
    #
    for zfrom in zones.itervalues():
        waiting_agents = set([agt for agt in zfrom.agents.itervalues() if agt.sim_state == WAITING])
        if not waiting_agents:
            continue
        demands = []
        for zto in zones.itervalues():
            num_demands = np.random.binomial(fl[zfrom.zid][zto.zid], Prob_SHOW)
            for _ in xrange(num_demands):
                demands.append(zto)
        shuffle(demands)
        if len(demands) < len(waiting_agents):
            agent_get_demand = sample(waiting_agents, len(demands))
        else:
            agent_get_demand = waiting_agents
        # Process agents who get demand
        for i, agt in enumerate(agent_get_demand):
            assert agt.zone_from == zfrom
            zones[agt.a].remove_agent(agt)
            agt.sim_state = POB
            agt.s1 = demands[i].zid
            agt.cost = Co[agt.a][agt.s1]
            agt.revenue = Re[agt.a][agt.s1]
            #
            push_event(Mt[agt.a][agt.s1], finish_transition, agt)
        # Process agents who do not get demand
        for agt in waiting_agents.difference(set(agent_get_demand)):
            agt.update_Q_sa()
            agt.s0, agt.a, agt.s1 = agt.a, None, None
            zones[agt.s0].add_agent(agt)
            agt.sim_state = IDLE
            #
            push_event(0, take_action, agt)
    push_event(1, on_demand_arrival, None)
    #
    if num_demand_generation % 10000 == 0:
        print 'The number of demands generation: %d' % num_demand_generation
        display_q_values()
    #
    if len(agents) == len([agt for agt in agents if agt.Q_convergence]):
        # End simulation
        print 'Finish simulation'
        print 'The number of demands generation: %d' % num_demand_generation
        display_q_values()
        finish_simulation()


def finish_transition(agt):
    agt.update_Q_sa()
    agt.s0, agt.a, agt.s1 = agt.s1, None, None
    zones[agt.s0].add_agent(agt)
    agt.sim_state = IDLE
    #
    push_event(0, take_action, agt)


def display_q_values():
    sa_statement = agents[0].keys()
    for agt in agents:
        for s in S:
            policy = []
            max_Q_value, max_a = -1e400, None
            for a in A:
                Q_sa_value = agt.Q_sa[s, a]
                if max_Q_value < Q_sa_value:
                    max_Q_value = Q_sa_value
                    max_a = a
            policy.append(max_a)
        print agt.aid, policy, [agt.Q_sa[sa] for sa in sa_statement]


class scg_zone(object):
    def __init__(self, zid):
        self.zid = zid
        self.agents, self.demands = {}, []

    def __repr__(self):
        return 'zid %d' % (self.zid)

    def add_agent(self, agt):
        self.agents[agt.aid] = agt

    def remove_agent(self, d):
        self.agents.pop(d.aid)


class scg_agent(object):
    def __init__(self, aid, s0):
        self.aid = aid
        self.s0, self.a, self.s1 = s0, None, None
        self.Q_sa = {}
        self.N_sas = {}
        for s0 in S:
            for a in A:
                self.Q_sa[s0, a] = 0.0
                for s1 in S:
                    self.N_sas[s0, a, s1] = 1
        self.Q_convergence = False
        self.revenue, self.cost = 0.0, 0.0
        self.sim_state = IDLE

    def __repr__(self):
        return '(aid %d (%s), (s0, a, s1) = (%s, %s, %s)' % \
               (self.aid, str(self.sim_state), str(self.s0), str(self.a), str(self.s1))

    def update_Q_sa(self):
        s0, a = self.s0, self.a
        s1 = self.s1 if self.s1 else self.s0
        #
        max_Q_value = -1e400
        for na in A:
            total_N_sas = sum([self.N_sas[s1, na, _s] for _s in S])
            for ns in S:
                weight = self.N_sas[s1, a, ns] / float(total_N_sas)
                ns_max_Q_value = max([self.Q_sa[ns, _a] for _a in A])
                if max_Q_value < weight * ns_max_Q_value:
                    max_Q_value = weight * ns_max_Q_value
        #
        Q_sa0 = self.Q_sa[s0, a]
        self.Q_sa[s0, a] += ALPH * ((self.revenue - self.cost) + GAMMA * max_Q_value - self.Q_sa[s0, a])
        #
        self.revenue, self.cost = 0.0, 0.0
        self.N_sas[s0, a, s1] += 1
        #
        self.Q_convergence = True if abs(Q_sa0 - self.Q_sa[s0, a]) < EPSILON else False


if __name__ == '__main__':
    from stochastic_congestion_games.problems import p10
    num_agents, num_zones, time_horizon, fl, Re, Co, Ds, d0, problem_saving_dir = p10()
    run(num_agents, num_zones, time_horizon, fl, Re, Co, Ds, d0, problem_saving_dir)