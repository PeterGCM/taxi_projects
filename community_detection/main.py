import __init__
#
from __init__ import grid_info_fn, get_processed_log_fn
from taxi_common.file_handling_functions import do_file_exist, load_picle_file
#
from classes import cd_zone
#
def run(time_from, time_to, zone_unit_km):
    #
    # Step 1. Split Singapore into zones
    #
    if not do_file_exist(grid_info_fn):
        from taxi_common.split_into_zones import run as run_split_into_zones #@UnresolvedImport
        hl_points, vl_points, zones = run_split_into_zones(zone_unit_km, cd_zone)
    else:
        hl_points, vl_points, zones = load_picle_file(grid_info_fn)
    #
    # Step 2. Preprocess logs 
    #
    processed_log_fn = get_processed_log_fn(time_from, time_to)
    if not do_file_exist(processed_log_fn):
        from preprocess_logs import run as run_preprocess_logs
        run_preprocess_logs(hl_points, vl_points, time_from, time_to)

    assert False

    #
    # Step 3. Count the number of relations 
    #
    relation_fn = get_relation_fn(processed_log_fn)
    if not do_file_exist(relation_fn):
        from count_linkages import run as run_count_relations
        did_relations = run_count_relations(processed_log_fn, zones)
    else:
        did_relations = load_picle_file(relation_fn)
    #
    # Step 4. Visualize relations 
    #
    from visualize_relations import run as run_visualize_relations
    run_visualize_relations(did_relations)
    
if __name__ == '__main__':
    run((2009, 1, 1, 0, 0, 30), (2009, 1, 1, 1, 0, 30), 0.5)
    
