from __future__ import division
import os, sys
#
sys.path.append(os.getcwd() + '/..')
#
MEMORY_MANAGE_INTERVAL = 24 * 60 * 60
COINCIDENCE_THRESHOLD_VALUE = 2
#
singapore_poly_fn = 'Singapore_polygon'
grid_info_fn = 'hl_vl_zones.pkl'
out_boundary_logs_fn = 'out_boundary.txt'
relation_prefix = 'relation-'
POB = 5
#
get_processed_log_fn = lambda time_from, time_to: 'processed-log-%s-%s.csv' % (str(time_from[0]) + ''.join(['%02d' % d for d in time_from[1:]]),
                                                                                  str(time_to[0]) + ''.join(['%02d' % d for d in time_from[1:]]))
def get_relation_fn(processed_log_fn):
    _, _, time_from, time_to = processed_log_fn[:-len('csv')].split('-')
    return 'relation-%s-%s' % (time_from, time_to)
