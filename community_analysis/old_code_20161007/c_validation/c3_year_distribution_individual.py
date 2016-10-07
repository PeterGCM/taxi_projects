import __init__
#
from community_analysis import all_trip_dir, all_trip_prefix
from community_analysis import year_dist_dir, individual_dist_fpath
#
from taxi_common.file_handling_functions import check_dir_create, save_pickle_file
#
import csv


def run():
    check_dir_create(year_dist_dir)
    #
    year_individual_count = {}
    for m in range(1, 12):
        yymm = '%02d%02d' % (9, m)
        print 'Handle the file; %s' % yymm
        with open('%s/%s%s.csv' % (all_trip_dir, all_trip_prefix, yymm), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h: i for i, h in enumerate(headers)}
            # hid = {'fare': 10, 'distance': 8, 'ei': 13, 'start-long': 4, 'ej': 14, 'did': 2, 'start-lat': 5, 'si': 11,
            #        'sj': 12, 'hh': 1, 'end-lat': 7, 'time': 0, 'duration': 9, 'end-long': 6, 'cn': 3}
            for row in reader:
                cn = row[hid['cn']]
                if cn == 'None':
                    continue
                did = int(row[hid['did']])
                hh, si, sj = int(row[hid['hh']]), int(row[hid['si']]), int(row[hid['sj']])
                if si < 0 or sj < 0:
                    continue
                if not year_individual_count.has_key(did):
                    year_individual_count[did] = {}
                    year_individual_count[did][hh, si, sj] = 0
                else:
                    if not year_individual_count[did].has_key((hh, si, sj)):
                        year_individual_count[did][hh, si, sj] = 0
                year_individual_count[did][hh, si, sj] += 1

    print 'aggregation'
    year_individual_prob = {}
    for did, hhij_numTrips in year_individual_count.iteritems():
        year_individual_prob[did] = {}
        sum_trip_num = sum(hhij_numTrips.values())
        for (hh, i, j), num_trips in hhij_numTrips.iteritems():
            year_individual_prob[did][hh, i, j] = num_trips / float(sum_trip_num)
    save_pickle_file(individual_dist_fpath, year_individual_prob)


if __name__ == '__main__':
    run()