import __init__
#
from community_analysis import com_dir, top5_com_dir
#
from taxi_common.file_handling_functions import get_all_directories, get_fn_from_dir, save_pickle_file, remove_create_dir
#
import networkx as nx
import csv


def run():
    remove_create_dir(top5_com_dir)
    #
    for dir_name in get_all_directories(com_dir):
        yyyy, str_CD, str_thD = dir_name.split('-')
        CD = int(str_CD[len('CD('):-len(')')])
        thD = int(str_thD[len('thD('):-len(')')])
        thD_dpath = '%s/%s' % (com_dir, dir_name)
        print thD_dpath
        summary_fpath = '%s/%s-CD(%d)-thD(%d)-community-summary.csv' % (thD_dpath, yyyy, CD, thD)
        com_sgth_fname = []
        with open(summary_fpath, 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            ts_header = None
            for k in hid.iterkeys():
                if k.startswith('tie-strength'):
                    ts_header = k
            assert ts_header
            for row in reader:
                com_sgth_fname.append([eval(row[hid[ts_header]]), row[hid['com-name']]])
        if len(com_sgth_fname) < 5:
            continue
        top_five_com = sorted(com_sgth_fname, reverse=True)[:5]
        top5_com_drivers = {}
        for _, cn in top_five_com:
            pkl_fpath = '%s/%s' % (thD_dpath, get_fn_from_dir(thD_dpath, '%s-CD(%d)-thD(%d)-%s'% (yyyy, CD, thD, cn), ''))
            top5_com_drivers[cn] = nx.read_gpickle(pkl_fpath).nodes()
        top5_com_drivers_fpath = '%s/%s-CD(%d)-thD(%d).pkl' % (top5_com_dir, yyyy, CD, thD)
        save_pickle_file(top5_com_drivers_fpath, top5_com_drivers)


if __name__ == '__main__':
    run()