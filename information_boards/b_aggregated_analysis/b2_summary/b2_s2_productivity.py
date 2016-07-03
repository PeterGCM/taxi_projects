import __init__  # @UnresolvedImport # @UnusedImport
#
from b_aggregated_analysis.__init__ import productivity_dir, productivity_prefix
from b_aggregated_analysis.__init__ import hourly_productivity_fn, zero_duration_timeslots
from __init__ import GENERAL, AIRPORT, NIGHTSAFARI
from __init__ import GEN_DUR, GEN_FARE, AP_DUR, AP_FARE, AP_QUEUE, NS_DUR, NS_FARE, NS_QUEUE
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, save_pickle_file
#
import datetime, csv


def run():
    cur_timestamp = datetime.datetime(2008, 12, 31, 23)
    last_timestamp = datetime.datetime(2011, 1, 1, 0)
    hp_summary, time_period_order = {}, []
    while cur_timestamp < last_timestamp:
        cur_timestamp += datetime.timedelta(hours=1)
        yyyy, mm, dd, hh = cur_timestamp.year, cur_timestamp.month, cur_timestamp.day, cur_timestamp.hour
        if yyyy == 2009 and mm == 12: continue
        if yyyy == 2010 and mm == 10: continue
        k = (str(yyyy - 2000), str(mm), str(dd), str(hh))
        hp_summary[k] = [0 for _ in range(len([GEN_DUR, GEN_FARE, \
                                                AP_DUR, AP_FARE, AP_QUEUE, \
                                                NS_DUR, NS_FARE, NS_QUEUE]))]
        time_period_order.append(k)
        #
    yy_l, mm_l, dd_l, hh_l = 'yy', 'mm', 'dd', 'hh'
    for fn in get_all_files(productivity_dir, productivity_prefix, '.csv'):
        with open('%s/%s' % (productivity_dir, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            hid = {h : i for i, h in enumerate(headers)}
            for row in reader:
                yy, mm, dd, hh = row[hid[yy_l]], row[hid[mm_l]], row[hid[dd_l]], row[hid[hh_l]]
                k = (yy, mm, dd, hh)
                if not hp_summary.has_key(k): continue
                hp_summary[k][GEN_DUR] += eval(row[hid['gen-duration']])
                hp_summary[k][GEN_FARE] += eval(row[hid['gen-fare']])
                hp_summary[k][AP_DUR] += eval(row[hid['ap-duration']])
                hp_summary[k][AP_FARE] += eval(row[hid['ap-fare']])
                hp_summary[k][AP_QUEUE] += eval(row[hid['ap-queueing-time']])
                hp_summary[k][NS_DUR] += eval(row[hid['ns-duration']])
                hp_summary[k][NS_FARE] += eval(row[hid['ns-fare']])
                hp_summary[k][NS_QUEUE] += eval(row[hid['ns-queueing-time']])
    # Summary
    print 'summary'
    zero_dur = []
    with open(hourly_productivity_fn, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'hh',
                    'gen-duration', 'gen-fare',
                    'ap-duration', 'ap-fare', 'ap-queueing-time',
                    'ns-duration', 'ns-fare', 'ns-queueing-time',
                    'gen-productivity',
                    'ap-productivity', 'ap-out-productivity',
                    'ns-productivity', 'ns-out-productivity']
        writer.writerow(header)
        for k in time_period_order:
            gen_dur, gen_fare, \
            ap_dur, ap_fare, ap_queue, \
            ns_dur, ns_fare, ns_queue = hp_summary[k]
            yy, mm, dd, hh = k
            #
            try:
                gen_prod = gen_fare / gen_dur
            except ZeroDivisionError:
                gen_prod = -1
                zero_dur.append([GENERAL, k])
                continue
            try:
                ap_prod = ap_fare / (ap_dur + ap_queue)
                ap_out_prod = (gen_fare - ap_fare) / (gen_dur - (ap_dur + ap_queue))
            except ZeroDivisionError:
                ap_prod = -1
                ap_out_prod = -1
                zero_dur.append([AIRPORT, k])
            try:
                ns_prod = ns_fare / (ns_dur + ns_queue)
                ns_out_prod = (gen_fare - ns_fare) / (gen_dur - (ns_dur + ns_queue))
            except ZeroDivisionError:
                ns_prod = -1
                ns_out_prod = -1
                zero_dur.append([NIGHTSAFARI, k])
            #
            writer.writerow([yy, mm, dd, hh,
                            gen_dur, gen_fare,
                            ap_dur, ap_fare, ap_queue,
                            ns_dur, ns_fare, ns_queue,
                            gen_prod,
                            ap_prod, ap_out_prod,
                            ns_prod, ns_out_prod])
    #
    save_pickle_file(zero_duration_timeslots, zero_dur)
    
if __name__ == '__main__':
    run()
