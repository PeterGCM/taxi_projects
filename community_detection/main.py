import __init__
#
from __init__ import grid_info_fn, get_processed_log_fn, linkage_dir
from taxi_common.file_handling_functions import check_file_exist, load_pickle_file, save_pickle_file
#
from _classes import cd_zone


def run(time_from, time_to, zone_unit_km):
    #
    # Step 1. Split Singapore into zones
    #
    print 'step 1'
    if not check_file_exist(grid_info_fn):
        from taxi_common.split_into_zones import run as run_split_into_zones
        hl_points, vl_points, zones = run_split_into_zones(zone_unit_km, cd_zone)
        save_pickle_file(grid_info_fn, [hl_points, vl_points, zones])
    else:
        hl_points, vl_points, zones = load_pickle_file(grid_info_fn)
    #
    # Step 2. Preprocess logs
    #
    print 'step 2'
    processed_log_fn = get_processed_log_fn(time_from, time_to)
    if not check_file_exist(processed_log_fn):
        from a_log_processing import run as run_preprocess_logs
        run_preprocess_logs(hl_points, vl_points, time_from, time_to)
    #
    # Step 3. Count the number of relations
    #
    print 'step 3'
    pkl_dir = linkage_dir + '/%d%02d%02d-%d%02d%02d' \
                            % (time_from[0], time_from[1],time_from[2],
                               time_to[0], time_to[1], time_to[2])
    if not check_file_exist(pkl_dir):
        from b_linkage import run as run_linkage
        run_linkage(processed_log_fn, zones)
    #
    # Step 4. Find pattern
    #
    print 'step 4'
    from c_pattern import run as run_pattern
    run_pattern(pkl_dir)
    #
    # Step 5. Visualize relations
    #
    # from d_graph import run as run_visualize_relations
    # run_visualize_relations(did_relations)
    
if __name__ == '__main__':
    run((2009, 1, 1, 0, 0, 0), (2009, 2, 1, 0, 0, 0), 0.5)
