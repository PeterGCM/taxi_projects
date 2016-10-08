import __init__
#
from community_analysis import dw_graph_dir, dw_graph_prefix, dw_summary_prefix
#
from taxi_common.file_handling_functions import check_path_exist, load_pickle_file, get_all_files, save_pickle_file
from taxi_common.charts import one_histogram


def run():
    for y in range(9, 13):
        yyyy = '20%02d' % y
        print 'Handle %s' % yyyy
        year_dw_summary_fpath = '%s/%s%s.csv' % (dw_graph_dir, dw_summary_prefix, yyyy)
        if check_path_exist(year_dw_summary_fpath):
            print 'The file had already been processed; %s' % yyyy
            continue

        year_dw_graph_fpath = '%s/%s%s.pkl' % (dw_graph_dir, dw_graph_prefix, yyyy)
        year_dw_graph = load_pickle_file(year_dw_graph_fpath)



    pass


if __name__ == '__main__':
    run()