import __init__
#
'''

'''
#
from community_analysis import taxi_home
#
from taxi_common.file_handling_functions import save_pickle_file
#
import csv

trip_normal_fpath = '%s/20%s/%s/trips/trips-%s-normal.csv' % (taxi_home, '09', '01', '0901')

hour_tripNum = {}
with open(trip_normal_fpath, 'rb') as tripFileN:
    tripReaderN = csv.reader(tripFileN)
    tripHeaderN = tripReaderN.next()
    # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3,
    #  'start-long': 4, 'start-lat': 5, 'end-long': 6, 'end-lat': 7,
    #  'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
    #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
    #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}
    hidN = {h: i for i, h in enumerate(tripHeaderN)}
    for rowN in tripReaderN:
        hour = int(rowN[hidN['start-hour']])
        if not hour_tripNum.has_key(hour):
            hour_tripNum[hour] = 0
        hour_tripNum[hour] += 1

save_pickle_file('_hour_tripNum.pkl', hour_tripNum)