from routing_pattern_performace import get_processed_trip_fn, get_timeslot

import csv, datetime, time

def run(x_points, y_points, time_from, time_to):
    tf_ts = time.mktime(datetime.datetime(*time_from).timetuple()) 
    tt_ts = time.mktime(datetime.datetime(*time_to).timetuple())
    #
    csv_files = get_csv_files(time_from, time_to)
    processed_log_fn = get_processed_trip_fn(time_from, time_to)
    with open(processed_log_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        writer.writerow(['time', 'did', 'state', 'i', 'j', 'timeslot', 'state-duration'])
        for fn1, fn2 in csv_files:
            with open(fn1, 'rb') as r_csvfile1:
                reader1 = csv.reader(r_csvfile1)
                headers1 = reader1.next()
                # {'trip-id': 0, 'job-id': 1, 'start-time': 2, 'end-time': 3, 'start-long': 4, 'start-lat': 5, 'end-long': 6,
                #  'end-lat': 7, 'vehicle-id': 8, 'distance': 9, 'fare': 10, 'duration': 11,
                #  'start-dow': 12, 'start-day': 13, 'start-hour': 14, 'start-minute': 15,
                #  'end-dow': 16, 'end-day': 17, 'end-hour': 18, 'end-minute': 19}  
                hid1 = {h : i for i, h in enumerate(headers1)}
                with open(fn2, 'rb') as r_csvfile2:
                    reader2 = csv.reader(r_csvfile2)
                    headers2 = reader2.next()
                    # {'start-zone': 0, 'end-zone': 1, 'start-postal': 2, 'driver-id': 4, 'end-postal': 3}
                    hid2 = {h : i for i, h in enumerate(headers2)}
                    print hid1
                    print hid2
    
def get_csv_files(time_from, time_to):
    #
    # TODO
    #
    return [('trips-0901-normal.csv', 'trips-0901-normal-ext.csv')]
