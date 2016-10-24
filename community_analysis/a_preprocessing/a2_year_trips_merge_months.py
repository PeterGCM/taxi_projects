import __init__
#
from community_analysis import ss_trips_dir, ss_trips_prefix
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files
#
import csv


def run():
    #
    for y in range(9, 13):
        ss_year_trips_fpath = '%s/%s20%02d.csv' % (ss_trips_dir, ss_trips_prefix, y)
        with open(ss_year_trips_fpath, 'wt') as w_csvfile:
            writer = csv.writer(w_csvfile, lineterminator='\n')
            writer.writerow(['did',
                             'timeFrame', 'zi', 'zj',
                             'groupName', 'prevDriver',
                             'time', 'day',
                             'start-long', 'start-lat',
                             'distance', 'duration', 'fare'])
        #
        for ss_trips_fpath in get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, y), '.csv'):
            with open(ss_trips_fpath, 'rb') as r_csvfile:
                reader = csv.reader(r_csvfile)
                headers = reader.next()
                hid = {h: i for i, h in enumerate(headers)}
                for row in reader:
                    t = eval(row[hid['time']])
                    cur_dt = datetime.datetime.fromtimestamp(t)
                    if handling_day != cur_dt.day:
                        logger.info('Processing %s %dth day' % (yymm, cur_dt.day))
                        for d in drivers.itervalues():
                            d.update_linkFrequency()
                        handling_day = cur_dt.day
                    did = int(row[hid['did']])
                    zi, zj = int(row[hid['zi']]), int(row[hid['zj']])
                try:
                    z = zones[(zi, zj)]
                except KeyError:
                    continue
                if not individual_year_distribution.has_key(did):
                    continue
                if not drivers.has_key(did):
                    drivers[did] = ca_driver_with_distribution(did, individual_year_distribution[did], individual_year_distribution[did])
                drivers[did].update_linkWeight(t, z)


