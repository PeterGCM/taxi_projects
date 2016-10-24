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
            for ss_trips_fpath in get_all_files(ss_trips_dir, '%s%02d' % (ss_trips_prefix, y), '.csv'):
                with open(ss_trips_fpath, 'rb') as r_csvfile:
                    reader = csv.reader(r_csvfile)
                    reader.next()
                    for row in reader:
                        writer.writerow(row)


if __name__ == '__main__':
    run()


