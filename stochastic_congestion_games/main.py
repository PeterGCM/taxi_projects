import __init__
#
from __init__ import init_inputs_fn
from problems import generate_problem
#
from MDPs.ddap import define_DDAP
from MDPs.algorithms import FP_SAP


#

#
def run():
    #
    # Input generation
    #

    #
    # Define Decision model for Agent Populations (DDAP)
    #
    PHI, R = define_DDAP(fl, Re, Co)
    #
    # Run Fictitious Play for Symmetric Agent Populations
    #
    _pi = FP_SAP(range(num_agents), range(num_zones), range(num_zones), PHI, R, H, d0)
    #
    # Display a problem and algorithm's result
    #


#     save_problem_policy(num_agents, num_zones, H, fl, Re, Co, d0, _pi)

if __name__ == '__main__':
    run()

