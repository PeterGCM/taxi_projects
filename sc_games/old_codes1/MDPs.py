import sc_games
#
from sc_games import taxi_data
from sc_games import ALPH, GAMMA, EPSILON
from sc_games import MAX_ITER_NUM
from sc_games import EXPLORE_DURATION
from sc_games import algo_names, get_current_pyname
from problems import sc_game0, sc_game1, sc_game2, sc_game3
#
from taxi_common.file_handling_functions import check_dir_create
#
import random, csv


def run(problem):
    num_agents, S, A, Tr_sas, R, ags_S = problem()
    #
    # Generate a initial policy for each agents
    #
    ags_poly = []
    for _ in range(num_agents):
        poly = {}
        for _s in S:
            for _ds in range(1, num_agents + 1):
                poly[_s, _ds, 0] = 1.0
                poly[_s, _ds, 1] = 0
        ags_poly.append(poly)
    #
    #
    #
    for i in range(num_agents):
        i_poly = ags_poly.pop(i)
        others_poly = ags_poly





    # Solve MDPs

if __name__ == '__main__':
    # for prob in [
    #     sc_game0,
    #     sc_game1,
    #     sc_game2,
    #     sc_game3
    # ]:
    #     run(prob)
    run(sc_game3)