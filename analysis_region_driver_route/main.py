from __future__ import division
#
from _setting import zone_visual_info_fn
from split_into_zones import run as run_split_into_zones
from visualizer import run as run_visualizer
# from process_log import run as process_log 
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
    if USE_VISUALIZER: 
        run_visualizer(singapore_poly_points, lines)
        

if __name__ == '__main__':
    run()