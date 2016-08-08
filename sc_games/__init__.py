import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'; check_dir_create(taxi_data)
#
SEED_NUM = 3
ALPH, GAMMA, EPSILON = .9, .9, .00000001
MAX_ITER_NUM = 100000
EXPLORE_DURATION = 2000

algo_names = {'Q_learning_states.py': 'Qst',
              'Q_learning_states1.py': 'Qst1',
              'Q_learning_actions.py': 'Qa',
              'Q_learning_simple.py': 'Qs'}

def get_current_pyname():
    return os.path.basename(sys.argv[0])