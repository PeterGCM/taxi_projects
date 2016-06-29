import __init__
#
from __init__ import grid_info_fn, get_processed_log_fn
from taxi_common.file_handling_functions import do_file_exist, load_picle_file, save_pickle_file
#
from _classes import cd_zone


def run(time_from, time_to, zone_unit_km):
    #
    # Step 1. Split Singapore into zones
    #
    if not do_file_exist(grid_info_fn):
        from taxi_common.split_into_zones import run as run_split_into_zones
        hl_points, vl_points, zones = run_split_into_zones(zone_unit_km, cd_zone)
        save_pickle_file(grid_info_fn, [hl_points, vl_points, zones])
    else:
        hl_points, vl_points, zones = load_picle_file(grid_info_fn)
    #
    # Step 2. Preprocess logs
    #
    processed_log_fn = get_processed_log_fn(time_from, time_to)
    if not do_file_exist(processed_log_fn):
        from a_log_processing import run as run_preprocess_logs
        run_preprocess_logs(hl_points, vl_points, time_from, time_to)
    #
    # Step 3. Count the number of relations
    #
    from b_linkage import run as run_linkage
    run_linkage(processed_log_fn, zones)


    #
    # Step 4. Visualize relations 
    #
    from d_graph import run as run_visualize_relations
    run_visualize_relations(did_relations)
    
if __name__ == '__main__':
    run((2009, 1, 1, 0, 0, 30), (2009, 1, 10, 1, 0, 30), 0.5)
    
