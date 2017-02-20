import __init__
#
'''

'''
#
from community_analysis import tfZ_TP_dpath, tfZ_TP_prefix
from community_analysis import dpaths, prefixs
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, get_fn_only, check_path_exist, save_pickle_file
from taxi_common.log_handling_functions import get_logger
#
import pandas as pd
from traceback import format_exc

logger = get_logger()


def run():
    check_dir_create(dpaths['baseline', '2009', 'countGraph'])
    #
    yyyy = '20%02d' % 9
    for tfZ_TP_fn in get_all_files(tfZ_TP_dpath, '%s%s*.csv' % (tfZ_TP_prefix, yyyy)):
        tfZ_TP_fpath = '%s/%s' % (tfZ_TP_dpath, tfZ_TP_fn)
        process_file(tfZ_TP_fpath)


def process_file(fpath):
    logger.info('Start handling; %s' % fpath)
    _, year, reducerID = get_fn_only(fpath)[:-len('.csv')].split('-')
    try:
        count_graph_dpath = dpaths['baseline', '2009', 'countGraph']
        count_graph_prefix = prefixs['baseline', '2009', 'countGraph']
        count_graph_fpath = '%s/%s%s.pkl' % (count_graph_dpath, count_graph_prefix, reducerID)
        #
        logger.info('Start loading; %s-%s' % (year, reducerID))
        df = pd.read_csv(fpath)
        count_graph = {}
        num_drivers = len(set(df['did']))
        for i, did1 in enumerate(set(df['did'])):
            if i % 10 == 0:
                logger.info('Doing regression %.2f; %s-%s' % (i / float(num_drivers), year, reducerID))
            did1_df = df[(df['did'] == did1)].copy(deep=True)

            did1_df = did1_df.drop(['month', 'day', 'timeFrame', 'zi', 'zj', 'tfZ', 'did', 'spendingTime'], axis=1)
            if '%d' % did1 in did1_df.columns:
                did1_df = did1_df.drop(['%d' % did1], axis=1)
            #
            for _did0, numPriorPresence in did1_df.sum().iteritems():
                if numPriorPresence == 0:
                    continue
                count_graph[int(_did0), did1] = numPriorPresence
        #
        logger.info('Start pickling; %s-%s' % (year, reducerID))
        save_pickle_file(count_graph_fpath, count_graph)
    except Exception as _:
        import sys
        with open('%s_%s.txt' % (sys.argv[0], '%s-%s' % (year, reducerID)), 'w') as f:
            f.write(format_exc())
        raise

if __name__ == '__main__':
    run()
