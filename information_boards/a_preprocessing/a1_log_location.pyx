import __init__
#
from information_boards import dpaths, prefixs
from information_boards import taxi_home
#
from taxi_common.geo_functions import get_ap_polygons, get_ns_polygon
from taxi_common.file_handling_functions import load_pickle_file, check_dir_create, check_path_exist
from taxi_common.log_handling_functions import get_logger
#
import csv
#
logger = get_logger()
#
of_dpath = dpaths['log']
of_prefixs = prefixs['log']
#
try:
    check_dir_create(of_dpath)
except OSError:
    pass


def run(yymm):
    ofpath = '%s/%s%s.csv' % (of_dpath, of_prefixs, yymm)
    if check_path_exist(ofpath):
        logger.info('The file had already been processed; %s' % yymm)
        return None
    logger.info('handle the file; %s' % yymm)
    yy, mm = yymm[:2], yymm[2:]
    log_fpath = '%s/20%s/%s/logs/logs-%s-normal.csv' % (taxi_home, yy, mm, yymm)
    ap_polygons, ns_polygon = get_ap_polygons(), get_ns_polygon()
    #
    with open(log_fpath, 'rb') as r_csvfile:
        reader = csv.reader(r_csvfile)
        headers = reader.next()
        hid = {h: i for i, h in enumerate(headers)}
        with open(ofpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            new_headers = ['time', 'vid', 'did', 'apBasePos', 'nsBasePos']
            writer.writerow(new_headers)
            #
            for row in reader:
                lon, lat = eval(row[hid['longitude']]), eval(row[hid['latitude']])
                apBasePos = 'X'
                for ap_polygon in ap_polygons:
                    res = ap_polygon.is_including((lon, lat))
                    if res:
                        apBasePos = ap_polygon.name
                        break
                nsBasePos = 'O' if ns_polygon.is_including((lon, lat)) else 'X'
                #
                new_row = [row[hid['time']], row[hid['vehicle-id']], row[hid['driver-id']],
                           apBasePos, nsBasePos]
                writer.writerow(new_row)
    logger.info('end the file; %s' % yymm)


if __name__ == '__main__':
    run()
