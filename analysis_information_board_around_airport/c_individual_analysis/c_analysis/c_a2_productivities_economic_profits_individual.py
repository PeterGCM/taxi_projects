from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import ftd_general_prod_db_for_ap, ftd_ap_prod_eco_prof_db
from supports._setting import ftd_general_prod_db_for_ns, ftd_ns_prod_eco_prof_db
from supports.etc_functions import check_dir_create, load_picle_file, write_text_file
#
from supports._setting import tables_dir, ftd_group_analysis
#
import numpy as np
from prettytable import PrettyTable
#

def run():
    def difference(data0, data1):
        diff = {}
        for k, v in data0.iteritems():
            diff[k] = data1[k] - v
        return diff
    check_dir_create(tables_dir)
    write_text_file(ftd_group_analysis, 'Init', True)
    #
    # Load data
    #
    y09_gen_d_prod_for_ap, y10_gen_d_prod_for_ap = load_picle_file(ftd_general_prod_db_for_ap)
    y09_gen_d_prod_for_ns, y10_gen_d_prod_for_ns = load_picle_file(ftd_general_prod_db_for_ns)
    (y09_piap_d_prod, y09_piap_d_eco_prof), \
    (y10_piap_d_prod, y10_piap_d_eco_prof), \
    (y09_poap_d_prod, y09_poap_d_eco_prof), \
    (y10_poap_d_prod, y10_poap_d_eco_prof) = load_picle_file(ftd_ap_prod_eco_prof_db)
    (y09_pins_d_prod, y09_pins_d_eco_prof), \
    (y10_pins_d_prod, y10_pins_d_eco_prof), \
    (y09_pons_d_prod, y09_pons_d_eco_prof), \
    (y10_pons_d_prod, y10_pons_d_eco_prof) = load_picle_file(ftd_ns_prod_eco_prof_db)
    #
    diffs_for_ap = {
            'diff_g_prod_for_ap'    : difference(y09_gen_d_prod_for_ap, y10_gen_d_prod_for_ap),
            #
            'diff_apin_prod' : difference(y09_piap_d_prod, y10_piap_d_prod),
            'diff_apout_prod': difference(y09_poap_d_prod, y10_poap_d_prod),
            'diff_apin_eco'  : difference(y09_piap_d_eco_prof, y10_piap_d_eco_prof),
            'diff_apout_eco' : difference(y09_poap_d_eco_prof, y10_poap_d_eco_prof),
            }
    
    diffs_for_ns = {
            'diff_g_prod_for_ns'    : difference(y09_gen_d_prod_for_ns, y10_gen_d_prod_for_ns),
            #
            'diff_nsin_prod' : difference(y09_pins_d_prod, y10_pins_d_prod),
            'diff_nsout_prod': difference(y09_pons_d_prod, y10_pons_d_prod),
            'diff_nsin_eco'  : difference(y09_pins_d_eco_prof, y10_pins_d_eco_prof),
            'diff_nsout_eco' : difference(y09_pons_d_eco_prof, y10_pons_d_eco_prof)
            }
    #
    write_text_file(ftd_group_analysis, 'Airport analysis ---------------------------------------------------')
    an_analysis(diffs_for_ap)
    write_text_file(ftd_group_analysis, '\nNight safari analysis ---------------------------------------------------')
    ns_analysis(diffs_for_ns)
    
def an_analysis(diffs_for_ap):
    summary('diff_g_prod_for_ap', diffs_for_ap)
    #
    summary('diff_apin_prod', diffs_for_ap)
    # 
    summary('diff_apout_prod', diffs_for_ap)
    # 
    summary('diff_apin_eco', diffs_for_ap)
    # 
    summary('diff_apout_eco', diffs_for_ap)


def ns_analysis(diffs_for_ns):
    summary('diff_g_prod_for_ns', diffs_for_ns)
    #
    summary('diff_nsin_prod', diffs_for_ns)
    # 
    summary('diff_nsout_prod', diffs_for_ns)
    # 
    summary('diff_nsin_eco', diffs_for_ns)
    # 
    summary('diff_nsout_eco', diffs_for_ns)

def summary(main_st, diffs):
    write_text_file(ftd_group_analysis, '----------------------------------------------- %s' % main_st)
    
    dids_values = diffs[main_st]
    #
    # Ordering
    #
    order_v_did = []
    for did, v in dids_values.iteritems():
        order_v_did.append([v, did])
    order_v_did.sort()
    order_v_did.reverse()
    #
    main_values = [v for v, _ in order_v_did]
    write_text_file(ftd_group_analysis, 'AVG: %f, STD: %f' % (np.mean(main_values), np.std(main_values)))
    high_group_range, middle_group_range, low_group_range = find_extreme_range(order_v_did), (0.45, 0.55), find_negative_range(order_v_did)
    data_ranges = [high_group_range, middle_group_range, low_group_range]
    hg_value, hg_did, mg_value, mg_did, lg_value, lg_did = grouping(data_ranges, order_v_did)
    main_group_data = [hg_value, mg_value, lg_value]
    main_group_keys = [hg_did, mg_did, lg_did]
    display_main_group(data_ranges, main_group_data)
    #
    for sub_st, sub_diff in diffs.iteritems():
        if sub_st == main_st: continue
        write_text_file(ftd_group_analysis, sub_st)
        sub_group_data = sub_grouping(main_group_keys, sub_diff)
        display_sub_group(sub_group_data)

def find_extreme_range(order_v_did):
    # more than mean's 50 percent
    values = [v for v, _ in order_v_did]
    mu, std = np.mean(values), np.std(values)
    i = 0
    while order_v_did[i][0] > mu + std * 2.0:
        i += 1
    return (0, i / len(order_v_did))

def find_negative_range(order_v_did):
    i = 0
    while order_v_did[i][0] >= 0:
        i += 1
    return (i / len(order_v_did), 1.0)

def display_main_group(data_ranges, main_group_data):
    _table = PrettyTable(["Main group", "M Per", "M AVG"])
    _table.align["M Per"] = "r"
    _table.align["M AVG"] = "r"
    for i, g_name in enumerate(['Extreme', 'Middle', 'Negative']):
        M_AVG = sum(main_group_data[i]) / len(main_group_data[i]) if main_group_data[i] else 0 
        _table.add_row([g_name,
                        '%.2f' % ((data_ranges[i][1] - data_ranges[i][0]) * 100),
                        '%.2f' % M_AVG])
    write_text_file(ftd_group_analysis, _table.get_string())
    
def display_sub_group(sub_group_data):
    _table = PrettyTable(["Main", "Sub", "S Per", "S AVG"])
    _table.align["S Per"] = "r"
    _table.align["S AVG"] = "r"
    m_g_names = ['Extreme', 'Middle', 'Negative']
    for i, (pg_value, ng_value) in enumerate(sub_group_data):
        main_g_name = m_g_names[i]
        if len(pg_value) != 0:
            S_Per = len(pg_value) / (len(pg_value) + len(ng_value)) * 100
            S_AVG = sum(pg_value) / len(pg_value)
        else:
            S_Per, S_AVG = 0, 0
        _table.add_row([main_g_name, 'Positive', '%.2f' % S_Per, '%.2f' % S_AVG])
        if len(ng_value) != 0:
            S_Per = len(ng_value) / (len(pg_value) + len(ng_value)) * 100
            S_AVG = sum(ng_value) / len(ng_value)
        else:
            S_Per, S_AVG = 0, 0
        _table.add_row([main_g_name, 'Negative',
                        '%.2f' % S_Per,
                        '%.2f' % S_AVG])
        S_AVG = sum(pg_value + ng_value) / len(pg_value + ng_value) if len(pg_value + ng_value) != 0 else 0
        _table.add_row([main_g_name, 'Summary',
                        '',
                        '%.2f' % S_AVG])
    write_text_file(ftd_group_analysis, _table.get_string())
    
def grouping(data_ranges, values_keys):
    high_group_range, middle_group_range, low_group_range = data_ranges
    total_num = len(values_keys)
    high_group = values_keys[int(high_group_range[0] * total_num):int(high_group_range[1] * total_num)]
    middle_group = values_keys[int(middle_group_range[0] * total_num):int(middle_group_range[1] * total_num)]
    low_group = values_keys[int(low_group_range[0] * total_num):int(low_group_range[1] * total_num)]
    #
    if high_group:
        hg_value, hg_did = zip(*high_group)
    else:
        hg_value, hg_did = [], []
    mg_value, mg_did = zip(*middle_group)
    if low_group:
        lg_value, lg_did = zip(*low_group)
    else:
        lg_value, lg_did = [], []
    return hg_value, hg_did, mg_value, mg_did, lg_value, lg_did

def sub_grouping(main_group_keys, _sub):
    sub_group_data = []
    for keys in main_group_keys:
        pg_value, ng_value = [], []
        for k in keys:
            v = _sub[k]
            if v >= 0:
                pg_value.append(v)
            else:
                ng_value.append(v)
        sub_group_data.append([pg_value, ng_value])
    return sub_group_data

if __name__ == '__main__':
    run()
