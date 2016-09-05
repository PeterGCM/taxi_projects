import __init__
#
from information_boards.c_individual_analysis import ftd_ap_stat_fpath, ftd_ap_linear_fpath
#
import pandas as pd
import csv


def run():
    ftd_ap_stat_df = pd.read_csv(ftd_ap_stat_fpath)
    Y09_drivers = set(ftd_ap_stat_df[(ftd_ap_stat_df['yy'] == 9)]['did'])
    Y10_drivers = set(ftd_ap_stat_df[(ftd_ap_stat_df['yy'] == 10)]['did'])

    by_drivers = Y09_drivers.intersection(Y10_drivers)
    filtered_ftd_df = ftd_ap_stat_df[ftd_ap_stat_df['did'].isin(by_drivers)]
    driver_stats = {}
    labels = ['all-num', 'all-dur', 'all-fare',
              'ap-num', 'ap-dur', 'ap-fare', 'ap-ep', 'ap-queueing-time',
              'apIn-num', 'apIn-dur', 'apIn-fare', 'apIn-ep', 'apIn-queueing-time',
              'apOut-num', 'apOut-dur', 'apOut-fare', 'apOut-ep', 'apOut-queueing-time']
    for did in by_drivers:
        driver_stats[did] = [[] for _ in labels]
    for i, label in enumerate(labels):
        total_num_trip_df = filtered_ftd_df.groupby(['did', 'yy']).sum()[label].to_frame('v').reset_index()
        for did, yy, v in total_num_trip_df.values:
            if yy == 9:
                assert len(driver_stats[did][i]) == 0
            else:
                assert len(driver_stats[did][i]) == 1
            driver_stats[did][i].append(v)
    with open(ftd_ap_linear_fpath, 'wb') as w_csvfile:
        writer = csv.writer(w_csvfile, lineterminator='\n')
        header = [
            'did',
            #
            # Total
            #
            'BY-all-total-trip-num', 'Y09-all-total-trip-num', 'Y10-all-total-trip-num', 'Diff-all-total-trip-num',
            'BY-gen-total-trip-num', 'Y09-gen-total-trip-num', 'Y10-gen-total-trip-num', 'Diff-gen-total-trip-num',
            'BY-ap-total-trip-num', 'Y09-ap-total-trip-num', 'Y10-ap-total-trip-num', 'Diff-ap-total-trip-num',
            'BY-apIn-total-trip-num', 'Y09-apIn-total-trip-num', 'Y10-apIn-total-trip-num', 'Diff-apIn-total-trip-num',
            'BY-apOut-total-trip-num', 'Y09-apOut-total-trip-num', 'Y10-apOut-total-trip-num', 'Diff-apOut-total-trip-num',
            #
            'BY-all-total-dur', 'Y09-all-total-dur', 'Y10-all-total-dur', 'Diff-all-total-dur',
            'BY-gen-total-dur', 'Y09-gen-total-dur', 'Y10-gen-total-dur', 'Diff-gen-total-dur',
            'BY-ap-total-dur', 'Y09-ap-total-dur', 'Y10-ap-total-dur', 'Diff-ap-total-dur',
            'BY-apIn-total-dur', 'Y09-apIn-total-dur', 'Y10-apIn-total-dur', 'Diff-apIn-total-dur',
            'BY-apOut-total-dur', 'Y09-apOut-total-dur', 'Y10-apOut-total-dur', 'Diff-apOut-total-dur',
            #
            'BY-all-total-fare', 'Y09-all-total-fare', 'Y10-all-total-fare', 'Diff-all-total-fare',
            'BY-gen-total-fare', 'Y09-gen-total-fare', 'Y10-gen-total-fare', 'Diff-gen-total-fare',
            'BY-ap-total-fare', 'Y09-ap-total-fare', 'Y10-ap-total-fare', 'Diff-ap-total-fare',
            'BY-apIn-total-fare', 'Y09-apIn-total-fare', 'Y10-apIn-total-fare', 'Diff-apIn-total-fare',
            'BY-apOut-total-fare', 'Y09-apOut-total-fare', 'Y10-apOut-total-fare', 'Diff-apOut-total-fare',
            #
            'BY-ap-total-economic-profit', 'Y09-ap-total-economic-profit', 'Y10-ap-total-economic-profit', 'Diff-ap-total-economic-profit',
            'BY-apIn-total-economic-profit', 'Y09-apIn-total-economic-profit', 'Y10-apIn-total-economic-profit', 'Diff-apIn-total-economic-profit',
            'BY-apOut-total-economic-profit', 'Y09-apOut-total-economic-profit', 'Y10-apOut-total-economic-profit', 'Diff-apOut-total-economic-profit',
            #
            'BY-ap-total-qtime', 'Y09-ap-total-qtime', 'Y10-ap-total-qtime', 'Diff-ap-total-qtime',
            'BY-apIn-total-qtime', 'Y09-apIn-total-qtime', 'Y10-apIn-total-qtime', 'Diff-apIn-total-qtime',
            'BY-apOut-total-qtime', 'Y09-apOut-total-qtime', 'Y10-apOut-total-qtime', 'Diff-apOut-total-qtime',
            #
            # Average
            #
            'BY-all-avg-dur-per-trip', 'Y09-all-avg-dur-per-trip', 'Y10-all-avg-dur-per-trip', 'Diff-all-avg-dur-per-trip',
            'BY-gen-avg-dur-per-trip', 'Y09-gen-avg-dur-per-trip', 'Y10-gen-avg-dur-per-trip', 'Diff-gen-avg-dur-per-trip',
            'BY-ap-avg-dur-per-trip', 'Y09-ap-avg-dur-per-trip', 'Y10-ap-avg-dur-per-trip', 'Diff-ap-avg-dur-per-trip',
            'BY-apIn-avg-dur-per-trip', 'Y09-apIn-avg-dur-per-trip', 'Y10-apIn-avg-dur-per-trip', 'Diff-apIn-avg-dur-per-trip',
            'BY-apOut-avg-dur-per-trip', 'Y09-apOut-avg-dur-per-trip', 'Y10-apOut-avg-dur-per-trip', 'Diff-apOut-avg-dur-per-trip',
            #
            'BY-all-avg-fare-per-trip', 'Y09-all-avg-fare-per-trip', 'Y10-all-avg-fare-per-trip', 'Diff-all-avg-fare-per-trip',
            'BY-gen-avg-fare-per-trip', 'Y09-gen-avg-fare-per-trip', 'Y10-gen-avg-fare-per-trip', 'Diff-gen-avg-fare-per-trip',
            'BY-ap-avg-fare-per-trip', 'Y09-ap-avg-fare-per-trip', 'Y10-ap-avg-fare-per-trip', 'Diff-ap-avg-fare-per-trip',
            'BY-apIn-avg-fare-per-trip', 'Y09-apIn-avg-fare-per-trip', 'Y10-apIn-avg-fare-per-trip', 'Diff-apIn-avg-fare-per-trip',
            'BY-apOut-avg-fare-per-trip', 'Y09-apOut-avg-fare-per-trip', 'Y10-apOut-avg-fare-per-trip', 'Diff-apOut-avg-fare-per-trip',
            #
            'BY-ap-avg-economic-profit-per-trip', 'Y09-ap-avg-economic-profit-per-trip', 'Y10-ap-avg-economic-profit-per-trip', 'Diff-ap-avg-economic-profit-per-trip',
            'BY-apIn-avg-economic-profit-per-trip', 'Y09-apIn-avg-economic-profit-per-trip', 'Y10-apIn-avg-economic-profit-per-trip', 'Diff-apIn-avg-economic-profit-per-trip',
            'BY-apOut-avg-economic-profit-per-trip', 'Y09-apOut-avg-economic-profit-per-trip', 'Y10-apOut-avg-economic-profit-per-trip', 'Diff-apOut-avg-economic-profit-per-trip',
            #
            'BY-ap-avg-qtime-per-trip', 'Y09-ap-avg-qtime-per-trip', 'Y10-ap-avg-qtime-per-trip', 'Diff-ap-avg-qtime-per-trip',
            'BY-apIn-avg-qtime-per-trip', 'Y09-apIn-avg-qtime-per-trip', 'Y10-apIn-avg-qtime-per-trip', 'Diff-apIn-avg-qtime-per-trip',
            'BY-apOut-avg-qtime-per-trip', 'Y09-apOut-avg-qtime-per-trip', 'Y10-apOut-avg-qtime-per-trip', 'Diff-apOut-avg-qtime-per-trip',
            #
            # Productivity
            #
            'BY-all-productivity', 'Y09-all-productivity', 'Y10-all-productivity', 'Diff-all-productivity',
            'BY-gen-productivity', 'Y09-gen-productivity', 'Y10-gen-productivity', 'Diff-gen-productivity',
            'BY-ap-productivity', 'Y09-ap-productivity', 'Y10-ap-productivity', 'Diff-ap-productivity',
            'BY-apIn-productivity', 'Y09-apIn-productivity', 'Y10-apIn-productivity', 'Diff-apIn-productivity',
            'BY-apOut-productivity', 'Y09-apOut-productivity', 'Y10-apOut-productivity', 'Diff-apOut-productivity',
            #
            # Etc.
            #
            'BY-proportion-all-num-by-ap-num', 'Y09-proportion-all-num-by-ap-num', 'Y10-proportion-all-num-by-ap-num', 'Diff-proportion-all-num-by-ap-num',
        ]
        writer.writerow(header)
        #
        print '# of full-time drivers: %d' % (len(driver_stats))
        for i, did in enumerate(sorted(driver_stats.keys())):
            if i % 100 == 0:
                print i, did
            (Y09_all_num, Y10_all_num), (Y09_all_dur, Y10_all_dur), (Y09_all_fare, Y10_all_fare) \
            , (Y09_ap_num, Y10_ap_num), (Y09_ap_dur, Y10_ap_dur), (Y09_ap_fare, Y10_ap_fare), (Y09_ap_ep, Y10_ap_ep), (Y09_ap_qtime, Y10_ap_qtime) \
            , (Y09_apIn_num, Y10_apIn_num), (Y09_apIn_dur, Y10_apIn_dur), (Y09_apIn_fare, Y10_apIn_fare), (Y09_apIn_ep, Y10_apIn_ep), (Y09_apIn_qtime, Y10_apIn_qtime) \
            , (Y09_apOut_num, Y10_apOut_num), (Y09_apOut_dur, Y10_apOut_dur), (Y09_apOut_fare, Y10_apOut_fare), (Y09_apOut_ep, Y10_apOut_ep), (Y09_apOut_qtime, Y10_apOut_qtime) \
                = driver_stats[did]
            # if Y09_all_num == 0 and Y10_all_num == 0:
            #     continue
            Y09_gen_num, Y10_gen_num = Y09_all_num - Y09_ap_num, Y10_all_num - Y10_ap_num
            Y09_gen_dur, Y10_gen_dur = Y09_all_dur - (Y09_ap_dur + Y09_ap_qtime), Y10_all_dur - (Y10_ap_dur + Y10_ap_qtime)
            Y09_gen_fare, Y10_gen_fare = Y09_all_fare - Y09_ap_fare, Y10_all_fare - Y10_ap_fare
            #
            # Total
            #
            by_all_num, diff_all_num = Y09_all_num + Y10_all_num, Y10_all_num - Y09_all_num
            by_gen_num, diff_gen_num = Y09_gen_num + Y10_gen_num, Y10_gen_num - Y09_gen_num
            by_ap_num, diff_ap_num = Y09_ap_num + Y10_ap_num, Y10_ap_num - Y09_ap_num
            by_apIn_num, diff_apIn_num = Y09_apIn_num + Y10_apIn_num, Y10_apIn_num - Y09_apIn_num
            by_apOut_num, diff_apOut_num = Y09_apOut_num + Y10_apOut_num, Y10_apOut_num - Y09_apOut_num
            #
            by_all_dur, diff_all_dur = Y09_all_dur + Y10_all_dur, Y10_all_dur - Y09_all_dur
            by_gen_dur, diff_gen_dur = Y09_gen_dur + Y10_gen_dur, Y10_gen_dur - Y09_gen_dur
            by_ap_dur, diff_ap_dur = Y09_ap_dur + Y10_ap_dur, Y10_ap_dur - Y09_ap_dur
            by_apIn_dur, diff_apIn_dur = Y09_apIn_dur + Y10_apIn_dur, Y10_apIn_dur - Y09_apIn_dur
            by_apOut_dur, diff_apOut_dur = Y09_apOut_dur + Y10_apOut_dur, Y10_apOut_dur - Y09_apOut_dur
            #
            by_all_fare, diff_all_fare = Y09_all_fare + Y10_all_fare, Y10_all_fare - Y09_all_fare
            by_gen_fare, diff_gen_fare = Y09_gen_fare + Y10_gen_fare, Y10_gen_fare - Y09_gen_fare
            by_ap_fare, diff_ap_fare = Y09_ap_fare + Y10_ap_fare, Y10_ap_fare - Y09_ap_fare
            by_apIn_fare, diff_apIn_fare = Y09_apIn_fare + Y10_apIn_fare, Y10_apIn_fare - Y09_apIn_fare
            by_apOut_fare, diff_apOut_fare = Y09_apOut_fare + Y10_apOut_fare, Y10_apOut_fare - Y09_apOut_fare
            #
            by_ap_ep, diff_ap_ep = Y09_ap_ep + Y10_ap_ep, Y10_ap_ep - Y09_ap_ep
            by_apIn_ep, diff_apIn_ep = Y09_apIn_ep + Y10_apIn_ep, Y10_apIn_ep - Y09_apIn_ep
            by_apOut_ep, diff_apOut_ep = Y09_apOut_ep + Y10_apOut_ep, Y10_apOut_ep - Y09_apOut_ep
            #
            by_ap_qtime, diff_ap_qtime = Y09_ap_qtime + Y10_ap_qtime, Y10_ap_qtime - Y09_ap_qtime
            by_apIn_qtime, diff_apIn_qtime = Y09_apIn_qtime + Y10_apIn_qtime, Y10_apIn_qtime - Y09_apIn_qtime
            by_apOut_qtime, diff_apOut_qtime = Y09_apOut_qtime + Y10_apOut_qtime, Y10_apOut_qtime - Y09_apOut_qtime
            #
            # Avg. duration
            #
            all_dur_num = [(by_all_dur, by_all_num), (Y09_all_dur, Y09_all_num),
                       (Y10_all_dur, Y10_all_num), (diff_all_dur, diff_all_num)]
            by_all_avg_dur, Y09_all_avg_dur, Y10_all_avg_dur, diff_all_avg_dur \
                = [dur / float(num) if num != 0 else 0 for dur, num in all_dur_num]
            #
            gen_dur_num = [(by_gen_dur, by_gen_num), (Y09_gen_dur, Y09_gen_num),
                       (Y10_gen_dur, Y10_gen_num), (diff_gen_dur, diff_gen_num)]
            by_gen_avg_dur, Y09_gen_avg_dur, Y10_gen_avg_dur, diff_gen_avg_dur \
                = [dur / float(num) if num != 0 else 0 for dur, num in gen_dur_num]
            #
            ap_dur_num = [(by_ap_dur, by_ap_num), (Y09_ap_dur, Y09_ap_num),
                       (Y10_ap_dur, Y10_ap_num), (diff_ap_dur, diff_ap_num)]
            by_ap_avg_dur, Y09_ap_avg_dur, Y10_ap_avg_dur, diff_ap_avg_dur \
                = [dur / float(num) if num != 0 else 0 for dur, num in ap_dur_num]
            #
            apIn_dur_num = [(by_apIn_dur, by_apIn_num), (Y09_apIn_dur, Y09_apIn_num),
                       (Y10_apIn_dur, Y10_apIn_num), (diff_apIn_dur, diff_apIn_num)]
            by_apIn_avg_dur, Y09_apIn_avg_dur, Y10_apIn_avg_dur, diff_apIn_avg_dur \
                = [dur / float(num) if num != 0 else 0 for dur, num in apIn_dur_num]
            #
            apOut_dur_num = [(by_apOut_dur, by_apOut_num), (Y09_apOut_dur, Y09_apOut_num),
                       (Y10_apOut_dur, Y10_apOut_num), (diff_apOut_dur, diff_apOut_num)]
            by_apOut_avg_dur, Y09_apOut_avg_dur, Y10_apOut_avg_dur, diff_apOut_avg_dur \
                = [dur / float(num) if num != 0 else 0 for dur, num in apOut_dur_num]
            #
            # Avg. fare
            #
            all_fare_num = [(by_all_fare, by_all_num), (Y09_all_fare, Y09_all_num),
                       (Y10_all_fare, Y10_all_num), (diff_all_fare, diff_all_num)]
            by_all_avg_fare, Y09_all_avg_fare, Y10_all_avg_fare, diff_all_avg_fare \
                = [fare / float(num) if num != 0 else 0 for fare, num in all_fare_num]
            #
            gen_fare_num = [(by_gen_fare, by_gen_num), (Y09_gen_fare, Y09_gen_num),
                       (Y10_gen_fare, Y10_gen_num), (diff_gen_fare, diff_gen_num)]
            by_gen_avg_fare, Y09_gen_avg_fare, Y10_gen_avg_fare, diff_gen_avg_fare \
                = [fare / float(num) if num != 0 else 0 for fare, num in gen_fare_num]
            #
            ap_fare_num = [(by_ap_fare, by_ap_num), (Y09_ap_fare, Y09_ap_num),
                       (Y10_ap_fare, Y10_ap_num), (diff_ap_fare, diff_ap_num)]
            by_ap_avg_fare, Y09_ap_avg_fare, Y10_ap_avg_fare, diff_ap_avg_fare \
                = [fare / float(num) if num != 0 else 0 for fare, num in ap_fare_num]
            #
            apIn_fare_num = [(by_apIn_fare, by_apIn_num), (Y09_apIn_fare, Y09_apIn_num),
                       (Y10_apIn_fare, Y10_apIn_num), (diff_apIn_fare, diff_apIn_num)]
            by_apIn_avg_fare, Y09_apIn_avg_fare, Y10_apIn_avg_fare, diff_apIn_avg_fare \
                = [fare / float(num) if num != 0 else 0 for fare, num in apIn_fare_num]
            #
            apOut_fare_num = [(by_apOut_fare, by_apOut_num), (Y09_apOut_fare, Y09_apOut_num),
                       (Y10_apOut_fare, Y10_apOut_num), (diff_apOut_fare, diff_apOut_num)]
            by_apOut_avg_fare, Y09_apOut_avg_fare, Y10_apOut_avg_fare, diff_apOut_avg_fare \
                = [fare / float(num) if num != 0 else 0 for fare, num in apOut_fare_num]
            #
            # Avg. economic profit
            #
            ap_ep_num = [(by_ap_ep, by_ap_num), (Y09_ap_ep, Y09_ap_num),
                       (Y10_ap_ep, Y10_ap_num), (diff_ap_ep, diff_ap_num)]
            by_ap_avg_ep, Y09_ap_avg_ep, Y10_ap_avg_ep, diff_ap_avg_ep \
                = [ep / float(num) if num != 0 else 0 for ep, num in ap_ep_num]
            #
            apIn_ep_num = [(by_apIn_ep, by_apIn_num), (Y09_apIn_ep, Y09_apIn_num),
                       (Y10_apIn_ep, Y10_apIn_num), (diff_apIn_ep, diff_apIn_num)]
            by_apIn_avg_ep, Y09_apIn_avg_ep, Y10_apIn_avg_ep, diff_apIn_avg_ep \
                = [ep / float(num) if num != 0 else 0 for ep, num in apIn_ep_num]
            #
            apOut_ep_num = [(by_apOut_ep, by_apOut_num), (Y09_apOut_ep, Y09_apOut_num),
                       (Y10_apOut_ep, Y10_apOut_num), (diff_apOut_ep, diff_apOut_num)]
            by_apOut_avg_ep, Y09_apOut_avg_ep, Y10_apOut_avg_ep, diff_apOut_avg_ep \
                = [ep / float(num) if num != 0 else 0 for ep, num in apOut_ep_num]
            #
            # Avg. queueting time
            #
            ap_qtime_num = [(by_ap_qtime, by_ap_num), (Y09_ap_qtime, Y09_ap_num),
                       (Y10_ap_qtime, Y10_ap_num), (diff_ap_qtime, diff_ap_num)]
            by_ap_avg_qtime, Y09_ap_avg_qtime, Y10_ap_avg_qtime, diff_ap_avg_qtime \
                = [qtime / float(num) if num != 0 else 0 for qtime, num in ap_qtime_num]
            #
            apIn_qtime_num = [(by_apIn_qtime, by_apIn_num), (Y09_apIn_qtime, Y09_apIn_num),
                       (Y10_apIn_qtime, Y10_apIn_num), (diff_apIn_qtime, diff_apIn_num)]
            by_apIn_avg_qtime, Y09_apIn_avg_qtime, Y10_apIn_avg_qtime, diff_apIn_avg_qtime \
                = [qtime / float(num) if num != 0 else 0 for qtime, num in apIn_qtime_num]
            #
            apOut_qtime_num = [(by_apOut_qtime, by_apOut_num), (Y09_apOut_qtime, Y09_apOut_num),
                       (Y10_apOut_qtime, Y10_apOut_num), (diff_apOut_qtime, diff_apOut_num)]
            by_apOut_avg_qtime, Y09_apOut_avg_qtime, Y10_apOut_avg_qtime, diff_apOut_avg_qtime \
                = [qtime / float(num) if num != 0 else 0 for qtime, num in apOut_qtime_num]
            #
            # Productivity
            #
            all_fare_dur = [(by_all_fare, by_all_dur), (Y09_all_fare, Y09_all_dur),
                         (Y10_all_fare, Y10_all_dur), (diff_all_fare, diff_all_dur)]
            by_all_productivity, Y09_all_productivity, Y10_all_productivity, diff_all_productivity \
                = [fare / float(dur) if dur != 0 else 0 for fare, dur in all_fare_dur]
            gen_fare_dur = [(by_gen_fare, by_gen_dur), (Y09_gen_fare, Y09_gen_dur),
                         (Y10_gen_fare, Y10_gen_dur), (diff_gen_fare, diff_gen_dur)]
            by_gen_productivity, Y09_gen_productivity, Y10_gen_productivity, diff_gen_productivity \
                = [fare / float(dur) if dur != 0 else 0 for fare, dur in gen_fare_dur]
            ap_fare_dur = [(by_ap_fare, by_ap_dur), (Y09_ap_fare, Y09_ap_dur),
                         (Y10_ap_fare, Y10_ap_dur), (diff_ap_fare, diff_ap_dur)]
            by_ap_productivity, Y09_ap_productivity, Y10_ap_productivity, diff_ap_productivity \
                = [fare / float(dur) if dur != 0 else 0 for fare, dur in ap_fare_dur]
            apIn_fare_dur = [(by_apIn_fare, by_apIn_dur), (Y09_apIn_fare, Y09_apIn_dur),
                         (Y10_apIn_fare, Y10_apIn_dur), (diff_apIn_fare, diff_apIn_dur)]
            by_apIn_productivity, Y09_apIn_productivity, Y10_apIn_productivity, diff_apIn_productivity \
                = [fare / float(dur) if dur != 0 else 0 for fare, dur in apIn_fare_dur]
            apOut_fare_dur = [(by_apOut_fare, by_apOut_dur), (Y09_apOut_fare, Y09_apOut_dur),
                         (Y10_apOut_fare, Y10_apOut_dur), (diff_apOut_fare, diff_apOut_dur)]
            by_apOut_productivity, Y09_apOut_productivity, Y10_apOut_productivity, diff_apOut_productivity \
                = [fare / float(dur) if dur != 0 else 0 for fare, dur in apOut_fare_dur]
            #
            # Etc.
            #
            all_num_ap_num = [(by_all_num, by_ap_num), (Y09_all_num, Y09_ap_num),
                         (Y10_all_num, Y10_ap_num), (diff_all_num, diff_ap_num)]
            by_ap_num_by_all_num, Y09_ap_num_by_all_num, Y10_ap_num_by_all_num, diff_ap_num_by_all_num \
                = [ap_num / float(all_num) if ap_num != 0 else 0 for all_num, ap_num in all_num_ap_num]

            new_row = [
                did,
                #
                # Total
                #
                by_all_num, Y09_all_num, Y10_all_num, diff_all_num,
                by_gen_num, Y09_gen_num, Y10_gen_num, diff_gen_num,
                by_ap_num, Y09_ap_num, Y10_ap_num, diff_ap_num,
                by_apIn_num, Y09_apIn_num, Y10_apIn_num, diff_apIn_num,
                by_apOut_num, Y09_apOut_num, Y10_apOut_num, diff_apOut_num,
                #
                by_all_dur, Y09_all_dur, Y10_all_dur, diff_all_dur,
                by_gen_dur, Y09_gen_dur, Y10_gen_dur, diff_gen_dur,
                by_ap_dur, Y09_ap_dur, Y10_ap_dur, diff_ap_dur,
                by_apIn_dur, Y09_apIn_dur, Y10_apIn_dur, diff_apIn_dur,
                by_apOut_dur, Y09_apOut_dur, Y10_apOut_dur, diff_apOut_dur,
                #
                by_all_fare, Y09_all_fare, Y10_all_fare, diff_all_fare,
                by_gen_fare, Y09_gen_fare, Y10_gen_fare, diff_gen_fare,
                by_ap_fare, Y09_ap_fare, Y10_ap_fare, diff_ap_fare,
                by_apIn_fare, Y09_apIn_fare, Y10_apIn_fare, diff_apIn_fare,
                by_apOut_fare, Y09_apOut_fare, Y10_apOut_fare, diff_apOut_fare,
                #
                by_ap_ep, Y09_ap_ep, Y10_ap_ep, diff_ap_ep,
                by_apIn_ep, Y09_apIn_ep, Y10_apIn_ep, diff_apIn_ep,
                by_apOut_ep, Y09_apOut_ep, Y10_apOut_ep, diff_apOut_ep,
                #
                by_ap_qtime, Y09_ap_qtime, Y10_ap_qtime, diff_ap_qtime,
                by_apIn_qtime, Y09_apIn_qtime, Y10_apIn_qtime, diff_apIn_qtime,
                by_apOut_qtime, Y09_apOut_qtime, Y10_apOut_qtime, diff_apOut_qtime,
                #
                # Average
                #
                by_all_avg_dur, Y09_all_avg_dur, Y10_all_avg_dur, diff_all_avg_dur,
                by_gen_avg_dur, Y09_gen_avg_dur, Y10_gen_avg_dur, diff_gen_avg_dur,
                by_ap_avg_dur, Y09_ap_avg_dur, Y10_ap_avg_dur, diff_ap_avg_dur,
                by_apIn_avg_dur, Y09_apIn_avg_dur, Y10_apIn_avg_dur, diff_apIn_avg_dur,
                by_apOut_avg_dur, Y09_apOut_avg_dur, Y10_apOut_avg_dur, diff_apOut_avg_dur,
                #
                by_all_avg_fare, Y09_all_avg_fare, Y10_all_avg_fare, diff_all_avg_fare,
                by_gen_avg_fare, Y09_gen_avg_fare, Y10_gen_avg_fare, diff_gen_avg_fare,
                by_ap_avg_fare, Y09_ap_avg_fare, Y10_ap_avg_fare, diff_ap_avg_fare,
                by_apIn_avg_fare, Y09_apIn_avg_fare, Y10_apIn_avg_fare, diff_apIn_avg_fare,
                by_apOut_avg_fare, Y09_apOut_avg_fare, Y10_apOut_avg_fare, diff_apOut_avg_fare,
                #
                by_ap_avg_ep, Y09_ap_avg_ep, Y10_ap_avg_ep, diff_ap_avg_ep,
                by_apIn_avg_ep, Y09_apIn_avg_ep, Y10_apIn_avg_ep, diff_apIn_avg_ep,
                by_apOut_avg_ep, Y09_apOut_avg_ep, Y10_apOut_avg_ep, diff_apOut_avg_ep,
                #
                by_ap_avg_qtime, Y09_ap_avg_qtime, Y10_ap_avg_qtime, diff_ap_avg_qtime,
                by_apIn_avg_qtime, Y09_apIn_avg_qtime, Y10_apIn_avg_qtime, diff_apIn_avg_qtime,
                by_apOut_avg_qtime, Y09_apOut_avg_qtime, Y10_apOut_avg_qtime, diff_apOut_avg_qtime,
                #
                # Productivity
                #
                by_all_productivity, Y09_all_productivity, Y10_all_productivity, diff_all_productivity,
                by_gen_productivity, Y09_gen_productivity, Y10_gen_productivity, diff_gen_productivity,
                by_ap_productivity, Y09_ap_productivity, Y10_ap_productivity, diff_ap_productivity,
                by_apIn_productivity, Y09_apIn_productivity, Y10_apIn_productivity, diff_apIn_productivity,
                by_apOut_productivity, Y09_apOut_productivity, Y10_apOut_productivity, diff_apOut_productivity,
                #
                # Etc.
                #
                by_ap_num_by_all_num, Y09_ap_num_by_all_num, Y10_ap_num_by_all_num, diff_ap_num_by_all_num
            ]
            writer.writerow(new_row)


if __name__ == '__main__':
    run()
