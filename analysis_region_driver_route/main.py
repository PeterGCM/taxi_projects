from __init__ import * #@UnusedWildImport
#
print taxi_data
from etc_functions import save_pickle_file
import sys
for p in sys.path:
    print p
import test.m1 
assert False
from _setting import zone_visual_info_fn
from split_into_zones import run as run_split_into_zones
# from visualizer import run as run_visualizer
from process_log import run as run_process_log 
#
import os, pickle
#
USE_VISUALIZER = False

assert False

def run():
    if not os.path.exists(zone_visual_info_fn):
        x_points, y_points, zones, singapore_poly_points, lines = run_split_into_zones()
        with open(zone_visual_info_fn, 'wb') as fp:
            pickle.dump([x_points, y_points, zones, singapore_poly_points, lines], fp)
    else:
        with open(zone_visual_info_fn, 'rb') as fp:
            x_points, y_points, zones, singapore_poly_points, lines = pickle.load(fp)
    run_process_log(x_points, y_points, zones, (2009, 1, 1, 0, 0, 0), (2009, 1, 10, 0, 0, 0))
#     if USE_VISUALIZER: 
#         run_visualizer(singapore_poly_points, lines)

def test():
    import os, sys  
    sys.path.append(os.getcwd() + '/../taxi_common')
    for p in sys.path:
        print p 
    import etc_functions
    print etc_functions.load_picle_file
    
    assert False
    with open('zone-driver-090101000030-090101010030.pkl', 'rb') as fp:
        drivers = pickle.load(fp)
    with open('result.txt', 'w') as f:
        for v in drivers:
            f.write(str(v) + '\n')
if __name__ == '__main__':
    test()
#     run()
