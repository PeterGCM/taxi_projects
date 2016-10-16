import __init__
#
from community_analysis._classes import ca_driver_with_com, ca_driver_with_distribution
from community_analysis import top5_com_dir, trip_dir, ctrip_dir, clink_dir
from community_analysis import generate_zones
from community_analysis import BY_COM_O, BY_COM_X
#
from taxi_common.file_handling_functions import get_all_files, check_dir_create, load_pickle_file, save_pickle_file
from taxi_common.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv


def run():
    check_dir_create(ctrip_dir)
    check_dir_create(clink_dir)
    #
    init_multiprocessor(11)
    count_num_jobs = 0
    for fn in get_all_files(top5_com_dir, '', '.pkl'):
        put_task(for_multiprocessor, [fn])
        count_num_jobs += 1
    end_multiprocessor(count_num_jobs)


def for_multiprocessor(fn):
    yyyy, str_CD, str_thD = fn[:-len('.pkl')].split('-')
    CD = int(str_CD[len('CD('):-len(')')])
    thD = int(str_thD[len('thD('):-len(')')])
    top5_com_drivers = load_pickle_file('%s/%s' % (top5_com_dir, fn))
    drivers = {}
    did_cn = {}
    for cn, com_drivers in top5_com_drivers.iteritems():
        for did in com_drivers:
            drivers[did] = ca_driver_with_com(did, com_drivers)
            did_cn[did] = cn
    ctrip_fn = '%s/%s-CD(%d)-thD(%d)-ctrip.csv' % (ctrip_dir, yyyy, CD, thD)
    with open(ctrip_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['time', 'yy', 'mm', 'did', 'cn', 'by_com',
                          'start-long', 'start-lat', 'end-long', 'end-lat',
                         'distance', 'duration', 'fare',
                         'si', 'sj', 'ei', 'ej'])
    #
    clink_thD_dpath = '%s/%s-CD(%d)-thD(%d)' % (clink_dir, yyyy, CD, thD)
    check_dir_create(clink_thD_dpath)
    for m in range(1, 12):
        yymm = '%02d%02d' % (int(yyyy) - 2000, m)
        print yymm

        yymm_dir = '%s/%s' % (trip_dir, yymm)
        zones = generate_zones()
        pairs_day_counting = {}
        num_day_in_month = 0
        for fn in get_all_files(yymm_dir, '', '.csv'):
            print fn
            num_day_in_month += 1
            with open('%s/%s' % (yymm_dir, fn), 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    did = int(row[hid['did']])
                    t = eval(row[hid['time']])
                    # Find a targeted zone
                    si, sj = int(row[hid['si']]), int(row[hid['sj']])
                    try:
                        z = zones[(si, sj)]
                        #
                        try:
                            assert z.check_validation()
                        except AssertionError:
                            pass
                    except KeyError:
                        pass
                    if not drivers.has_key(did): drivers[did] = ca_driver_with_distribution(did)
                    by_com = drivers[did].update_linkage(t, z)
                    #
                    if did_cn.has_key(did):
                        cn = did_cn[did]
                        assert (by_com == BY_COM_O) or (by_com == BY_COM_X), by_com
                        with open(ctrip_fn, 'a') as w_csvfile:
                            writer = csv.writer(w_csvfile, lineterminator='\n')
                            new_row = [
                                row[hid['time']], yymm[:2], yymm[-2:], row[hid['did']], cn, by_com,
                                row[hid['start-long']], row[hid['start-lat']], row[hid['end-long']],
                                row[hid['end-lat']],
                                row[hid['distance']], row[hid['duration']], row[hid['fare']],
                                row[hid['si']], row[hid['sj']], row[hid['ei']], row[hid['ej']]
                            ]
                            writer.writerow(new_row)
            day_pairs = set()
            for did0, d in drivers.iteritems():
                for did1, num_linkage in d.linkage.iteritems():
                    if (not did_cn.has_key(did0)) and (not did_cn.has_key(did0)):
                        continue
                    day_pairs.add((did0, did1))
                d.init_linkage()
            #
            for did0, did1 in day_pairs:
                if not pairs_day_counting.has_key((did0, did1)):
                    pairs_day_counting[(did0, did1)] = 0
                pairs_day_counting[(did0, did1)] += 1
        clink_fpath = '%s/%s-CD(%d)-clink.pkl' % (clink_thD_dpath, yymm, num_day_in_month)
        save_pickle_file(clink_fpath, pairs_day_counting)



if __name__ == '__main__':
    run()