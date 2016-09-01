import routing_pattern_performace
from classes import rp_zone
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file
#
def run(time_from, time_to):
    #
    # Step 1. Split Singapore into zones
    #
    if not check_path_exist(grid_info_fn):
        from taxi_common.sg_grid_zone import run as run_split_into_zones  # @UnresolvedImport
        hl_points, vl_points, zones = run_split_into_zones(rp_zone)
    else:
        hl_points, vl_points, zones = load_pickle_file(grid_info_fn)
    #
    # Step 2. Preprocess logs
    #
    processed_log_fn = get_processed_log_fn(time_from, time_to)
    if not check_path_exist(processed_log_fn):
        from preprocess_logs import run as run_preprocess_logs
        run_preprocess_logs(hl_points, vl_points, time_from, time_to)
    #
    # Step 3. Preprocess trips
    #
    processed_trip_fn = get_processed_trip_fn(time_from, time_to)
    if not check_path_exist(processed_trip_fn):
        from preprocess_trips import run as run_preprocess_trips 
        run_preprocess_trips(hl_points, vl_points, time_from, time_to)

if __name__ == '__main__':
    run((2009, 1, 1, 0, 0, 30), (2009, 1, 1, 1, 0, 30)) 
    
