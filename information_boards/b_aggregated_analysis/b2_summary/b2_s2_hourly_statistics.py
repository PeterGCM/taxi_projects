import __init__
#
from information_boards.b_aggregated_analysis.b2_summary import ALL_DUR, ALL_FARE, ALL_NUM
from information_boards.b_aggregated_analysis.b2_summary import AP_DUR, AP_FARE, AP_QUEUE, AP_NUM
from information_boards.b_aggregated_analysis.b2_summary import NS_DUR, NS_FARE, NS_QUEUE, NS_NUM
from information_boards.b_aggregated_analysis.b2_summary import ALL, AP, AP_GEN, NS, NS_GEN
from information_boards.b_aggregated_analysis import productivity_dir, productivity_prefix
from information_boards.b_aggregated_analysis import hourly_stats_fpath
from information_boards import AM2, AM5
from information_boards import error_hours
#
from taxi_common.file_handling_functions import check_dir_create, get_all_files, save_pickle_file
#
import datetime, csv


def run():
    ignoring_periods = []
    for ys, ms, ds, hs in error_hours:
        yyyy = 2000 + int(ys)
        mm, dd, hh = map(int, [ms, ds, hs])
        k = (yyyy, mm, dd, hh)
        ignoring_periods.append(k)
    cur_timestamp = datetime.datetime(2008, 12, 31, 23)
    last_timestamp = datetime.datetime(2011, 1, 1, 0)
    hp_summary, time_period_order = {}, []
    while cur_timestamp < last_timestamp:
        cur_timestamp += datetime.timedelta(hours=1)
        yyyy, mm, dd, hh = cur_timestamp.year, cur_timestamp.month, cur_timestamp.day, cur_timestamp.hour
        if yyyy == 2009 and mm == 12: continue
        if yyyy == 2010 and mm == 10: continue
        if yyyy == 2011: continue
        if AM2 <= hh and hh <= AM5: continue
        need2skip = False
        for ys, ms, ds, hs in error_hours:
            yyyy0 = 2000 + int(ys)
            mm0, dd0, hh0 = map(int, [ms, ds, hs])
            if (yyyy == yyyy0) and (mm == mm0) and (dd == dd0) and (hh == hh0):
                need2skip = True
        if need2skip: continue
        #
        k = (str(yyyy - 2000), str(mm), str(dd), str(hh))
        hp_summary[k] = [0 for _ in range(len([ALL_DUR, ALL_FARE, ALL_NUM, \
                                               AP_DUR, AP_FARE, AP_QUEUE, AP_NUM, \
                                               NS_DUR, NS_FARE, NS_QUEUE, NS_NUM]))]
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
                hp_summary[k][ALL_DUR] += eval(row[hid['all-duration']])
                hp_summary[k][ALL_FARE] += eval(row[hid['all-fare']])
                hp_summary[k][ALL_NUM] += eval(row[hid['all-num']])

                hp_summary[k][AP_DUR] += eval(row[hid['ap-duration']])
                hp_summary[k][AP_FARE] += eval(row[hid['ap-fare']])
                hp_summary[k][AP_QUEUE] += eval(row[hid['ap-queueing-time']])
                hp_summary[k][AP_NUM] += eval(row[hid['ap-num']])

                hp_summary[k][NS_DUR] += eval(row[hid['ns-duration']])
                hp_summary[k][NS_FARE] += eval(row[hid['ns-fare']])
                hp_summary[k][NS_QUEUE] += eval(row[hid['ns-queueing-time']])
                hp_summary[k][NS_NUM] += eval(row[hid['ns-num']])

    # Summary
    print 'summary'
    zero_dur = []
    with open(hourly_stats_fpath, 'wt') as w_csvfile:
        writer = csv.writer(w_csvfile)
        header = ['yy', 'mm', 'dd', 'hh',
                    'all-num',
                        'all-total-duration', 'all-avg-duration',
                        'all-total-fare', 'all-avg-fare',
                        'all-productivity',
                    'ap-num',
                        'atotal-duration', 'aavg-duration',
                        'atotal-fare', 'aavg-fare',
                        'atotal-queueing', 'aavg-queueing',
                        'ap-productivity',
                    'ap-gen-num',
                        'ap-gtotal-duration', 'ap-gavg-duration',
                        'ap-gtotal-fare', 'ap-gavg-fare',
                        'ap-gen-productivity',
                    'ns-num',
                        'ntotal-duration', 'navg-duration',
                        'ntotal-fare', 'navg-fare',
                        'ntotal-queueing', 'navg-queueing',
                        'ns-productivity',
                    'ns-gen-num',
                        'ns-gtotal-duration', 'ns-gavg-duration',
                        'ns-gtotal-fare', 'ns-gavg-fare',
                        'ns-gen-productivity',
                     'key']
        writer.writerow(header)
        for k in time_period_order:
            all_total_dur, all_total_fare, all_num, \
            ap_total_dur, ap_total_fare, ap_total_queue, ap_num, \
            ns_total_dur, ns_total_fare, ns_total_queue, ns_num = hp_summary[k]
            #
            if all_num == 0:
                all_avg_dur, all_avg_fare = -1, -1
                all_prod = -1
            else:
                all_avg_dur, all_avg_fare = all_total_dur / float(all_num), all_total_fare / float(all_num)
                if all_total_dur == 0:
                    zero_dur.append([ALL, k])
                    all_prod = -1
                else:
                    all_prod = all_total_fare / float(all_total_dur)
            #
            yy, mm, dd, hh = k
            if ap_num == 0:
                ap_avg_dur, ap_avg_fare, ap_avg_queue = -1, -1, -1
                ap_prod = -1
            else:
                ap_avg_dur, ap_avg_fare, ap_avg_queue = \
                    ap_total_dur / float(ap_num), ap_total_fare / float(ap_num), ap_total_queue / float(ap_num)
                if ap_total_dur == 0:
                    zero_dur.append([AP, k])
                    ap_prod = -1
                else:
                    ap_prod = ap_total_fare / float(ap_total_dur)
            ap_gen_num = all_num - ap_num
            ap_gen_total_dur = all_total_dur - (ap_total_dur + ap_total_queue)
            ap_gen_total_fare = all_total_fare - ap_total_fare
            if ap_gen_num == 0:
                ap_gen_avg_dur, ap_gen_avg_fare = -1, -1
                ap_gen_prod = -1
            else:
                ap_gen_avg_dur, ap_gen_avg_fare = \
                    ap_gen_total_dur / float(ap_gen_num), ap_gen_total_fare / float(ap_gen_num)
                if ap_gen_total_dur == 0:
                    zero_dur.append([AP_GEN, k])
                    ap_gen_prod = -1
                else:
                    ap_gen_prod = ap_gen_total_fare / float(ap_gen_total_dur)
            #
            if ns_num == 0:
                ns_avg_dur, ns_avg_fare, ns_avg_queue = -1, -1, -1
                ns_prod = -1
            else:
                ns_avg_dur, ns_avg_fare, ns_avg_queue = \
                    ns_total_dur / float(ns_num), ns_total_fare / float(ns_num), ns_total_queue / float(ns_num)
                if ns_total_dur == 0:
                    zero_dur.append([NS, k])
                    ns_prod = -1
                else:
                    ns_prod = ns_total_fare / float(ns_total_dur)
            ns_gen_num = all_num - ns_num
            ns_gen_total_dur = all_total_dur - (ns_total_dur + ns_total_queue)
            ns_gen_total_fare = all_total_fare - ns_total_fare
            if ns_gen_num == 0:
                ns_gen_avg_dur, ns_gen_avg_fare = -1, -1
                ns_gen_prod = -1
            else:
                ns_gen_avg_dur, ns_gen_avg_fare = \
                    ns_gen_total_dur / float(ns_gen_num), ns_gen_total_fare / float(ns_gen_num)
                if ns_gen_total_dur == 0:
                    zero_dur.append([NS_GEN, k])
                    ns_gen_prod = -1
                else:
                    ns_gen_prod = ns_gen_total_fare / float(ns_gen_total_dur)
            #
            writer.writerow([yy, mm, dd, hh,
                             all_num,
                                all_total_dur, all_avg_dur,
                                all_total_fare, all_avg_fare,
                                all_prod,
                             ap_num,
                                ap_total_dur, ap_avg_dur,
                                ap_total_fare, ap_avg_fare,
                                ap_total_queue, ap_avg_queue,
                                ap_prod,
                             ap_gen_num,
                                ap_gen_total_dur, ap_gen_avg_dur,
                                ap_gen_total_fare, ap_gen_avg_fare,
                                ap_gen_prod,
                             ns_num,
                                ns_total_dur, ap_avg_dur,
                                ns_total_fare, ns_avg_fare,
                                ns_total_queue, ns_avg_queue,
                                ns_prod,
                             ns_gen_num,
                                ns_gen_total_dur, ap_gen_avg_dur,
                                ns_gen_total_fare, ns_gen_avg_fare,
                                ns_gen_prod,
                             k])

    
if __name__ == '__main__':
    from traceback import format_exc

    try:
        run()
    except Exception as _:
        with open('logging_Python.txt', 'w') as f:
            f.write(format_exc())
        raise