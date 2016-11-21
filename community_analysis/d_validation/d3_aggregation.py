

def run():
    check_dir_create(dw_graph_dir)
    #
    for y in range(9, 13):
        yyyy = '20%02d' % y
        logger.info('Handle %s' % yyyy)
        year_aggregation_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_prefix, yyyy)
        if check_path_exist(year_aggregation_fpath):
            return None