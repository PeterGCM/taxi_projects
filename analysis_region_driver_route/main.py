from __future__ import division
#
from _setting import zone_visual_info_fn
from split_into_zones import run as run_split_into_zones
# from visualizer import run as run_visualizer
from process_log import run as run_process_log 
#
import os, pickle
#
USE_VISUALIZER = False

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
    with open('zone-driver-090101000030-090101000030.pkl', 'rb') as fp:
        zones, drivers = pickle.load(fp)
    print len(zones), len(drivers)
    count = 0
    for pos, z in zones.iteritems():
        print z.num_visit
        count += 1
        if count == 5:
            break
    count = 0
    for did, d in drivers.iteritems():
        print d.relation
        count += 1
        if count == 5:
            break    
        
#     print d
    

if __name__ == '__main__':
#     test()
    run()
