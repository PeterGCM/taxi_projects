import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/..')
#
from taxi_common.__init__ import get_taxi_home_path
taxi_home = get_taxi_home_path()
#
from taxi_common.file_handling_functions import check_dir_create
taxi_data = os.path.dirname(os.path.realpath(__file__)) + '/data'; check_dir_create(taxi_data)
#
R_CONSTANT, R_LINEAR, R_INVERSE, R_EXPONENTIAL = range(4)
rtype_rname = {
    R_CONSTANT: 'C',
    R_LINEAR: 'L',
    R_INVERSE: 'I',
    R_EXPONENTIAL: 'E'
}
T_SIMPLE, T_COMPLEX = range(2)
ttype_tname = {
    T_SIMPLE: 'S',
    T_COMPLEX: 'C'
}
#
SH_PARAMETER, SH_REWARD, SH_TRANSITION = range(3)
sheet_names = {
    SH_PARAMETER:   'Parameter',
    SH_REWARD:      'Reward',
    SH_TRANSITION:  'Transition'
}
PAR_L_ID_NUM_AGENT, PAR_L_ID_NUM_STATE, PAR_L_ID_DS, PAR_L_ID_R_TYPE, PAR_L_ID_Tr_TYPE, PAR_L_ID_AC = range(6)
parameter_labels = {
    PAR_L_ID_NUM_AGENT: '# of agents',
    PAR_L_ID_NUM_STATE: '# of states',
    PAR_L_ID_DS: 'DS',
    PAR_L_ID_R_TYPE:    'Reward type',
    PAR_L_ID_Tr_TYPE:   'Transition type',
    PAR_L_ID_AC:        'AC'
}
#
SEED_NUM = 3
ALPH, GAMMA, EPSILON = .9, .9, .00000001
MAX_ITER_NUM = 50000
NUM_SIMULATION, WARMUP_ITER = 100, 5000
BIG_M = 200
EXPLORE_DURATION = MAX_ITER_NUM * 0.4


def get_current_pyname():
    return os.path.basename(sys.argv[0])