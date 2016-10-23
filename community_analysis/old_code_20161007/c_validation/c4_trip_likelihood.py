import __init__
#
from community_analysis._classes import ca_driver_with_com_prevD
from community_analysis import all_trip_dir, all_trip_prefix
from community_analysis import year_dist_dir, individual_dist_fpath
from community_analysis import trip_likelihood_fpath
from community_analysis import top5_com_dir
from community_analysis import generate_zones
#
from taxi_common.file_handling_functions import check_dir_create, load_pickle_file, get_all_files
#
import pandas as pd
import csv


def run():
    check_dir_create(all_trip_dir)
    #
    com_dist = {}
    print 'Calculate com_dist'
    for com_dist_fn in get_all_files(year_dist_dir, '2009-trip-counting-COM', '.csv'):
        _, _, _, cn = com_dist_fn[:-len('.csv')].split('-')
        com_dist[cn] = {}
        df = pd.read_csv('%s/%s' % (year_dist_dir, com_dist_fn))
        all_num_trip = df['num-trips'].sum()
        df['prob.'] = df['num-trips'].apply(lambda x: x / float(all_num_trip))
        for tf, zid, _, prob in df.values:
            i, j = int(zid[len('z'):len('z###')]), int(zid[-len('###'):])
            assert i < 100 and j < 100, (i, j)
            com_dist[cn][tf, i, j] = prob
    print 'individual_prob loading'
    year_individual_prob = load_pickle_file(individual_dist_fpath)
    #
    top5_com_drivers = load_pickle_file('%s/%s' % (top5_com_dir, '2009-CD(184)-thD(92).pkl'))
    drivers = {}
    did_cn = {}
    for cn, com_drivers in top5_com_drivers.iteritems():
        for did in com_drivers:
            drivers[did] = ca_driver_with_com_prevD(did, com_drivers)
            did_cn[did] = cn
    #
    with open(trip_likelihood_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        writer.writerow(['time', 'did', 'cn', 'hh', 'si', 'sj',
                         'D-prob.(P1)', 'C-prob(P2)',
                         'max(0, P2-P1)', 'prevD'])
    #
    for m in range(1, 12):
        yymm = '%02d%02d' % (9, m)
        print 'Handle the file; %s' % yymm
        zones = generate_zones()
        with open('%s/%s%s.csv' % (all_trip_dir, all_trip_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            # hid = {'fare': 10, 'distance': 8, 'ei': 13, 'start-long': 4, 'ej': 14, 'did': 2, 'start-lat': 5, 'si': 11,
            #        'sj': 12, 'hh': 1, 'end-lat': 7, 'time': 0, 'duration': 9, 'end-long': 6, 'cn': 3}
            for row in reader:
                t = eval(row[hid['time']])
                cn = row[hid['cn']]
                if cn == 'None':
                    continue
                did = int(row[hid['did']])
                hh, si, sj = int(row[hid['hh']]), int(row[hid['si']]), int(row[hid['sj']])
                try:
                    z = zones[(si, sj)]
                    #
                    try:
                        assert z.check_validation()
                    except AssertionError:
                        pass
                except KeyError:
                    pass
                prevD = drivers[did].update_linkWeight(t, z)
                d_prob = year_individual_prob[did][hh, si, sj]
                c_prob = com_dist[cn][hh, si, sj]
                #
                with open(trip_likelihood_fpath, 'a') as w_csvfile:
                    writer = csv.writer(w_csvfile, lineterminator='\n')
                    new_row = [t, did, cn, hh, si, sj,
                               d_prob, c_prob,
                               max(0, c_prob - d_prob), prevD]
                    writer.writerow(new_row)


if __name__ == '__main__':
    run()