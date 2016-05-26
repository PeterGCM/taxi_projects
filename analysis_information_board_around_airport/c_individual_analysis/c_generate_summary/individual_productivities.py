from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import individual_detail_dir
from supports._setting import HOUR, CENT, PROD_LIMIT
from supports.etc_functions import save_pickle_file, load_picle_file
from supports.etc_functions import get_all_files
from supports._setting import for_full_driver_dir
#
import pandas as pd
import numpy as np
import csv
#
def run():
    Y09_general = pd.read_csv('%s/Y09-individual-general.csv' % (individual_detail_dir))
    Y10_general = pd.read_csv('%s/Y10-individual-general.csv' % (individual_detail_dir))
    Y09_prev_in = pd.read_csv('%s/Y09-individual-prev-in-ap.csv' % (individual_detail_dir))
    Y10_prev_in = pd.read_csv('%s/Y10-individual-prev-in-ap.csv' % (individual_detail_dir))
    Y09_prev_out = pd.read_csv('%s/Y09-individual-prev-out-ap.csv' % (individual_detail_dir))
    Y10_prev_out = pd.read_csv('%s/Y10-individual-prev-out-ap.csv' % (individual_detail_dir))
    #
    Y09_prev_in = Y09_prev_in[(Y09_prev_in['ap-prod'] < PROD_LIMIT)]
    Y09_prev_in = Y09_prev_in[(0 < Y09_prev_in['op-cost'])]
    Y10_prev_in = Y10_prev_in[(Y10_prev_in['ap-prod'] < PROD_LIMIT)]
    Y10_prev_in = Y10_prev_in[(0 < Y10_prev_in['op-cost'])]
    #
    Y09_prev_out = Y09_prev_out[(Y09_prev_out['ap-prod'] < PROD_LIMIT)]
    Y09_prev_out = Y09_prev_out[(0 < Y09_prev_out['op-cost'])]
    Y10_prev_out = Y10_prev_out[(Y10_prev_out['ap-prod'] < PROD_LIMIT)]
    Y10_prev_out = Y10_prev_out[(0 < Y10_prev_out['op-cost'])]
    # both years
    Y09_general_did, Y10_general_did = set(Y09_general['did']), set(Y10_general['did'])
    general_both_years_full_drivers = Y09_general_did.intersection(Y10_general_did)
    Y09_prev_in_did, Y10_prev_in_did = set(Y09_prev_in['did']), set(Y10_prev_in['did'])
    prev_in_both_years_full_drivers = Y09_prev_in_did.intersection(Y10_prev_in_did)
    Y09_prev_out_did, Y10_prev_out_did = set(Y09_prev_out['did']), set(Y10_prev_out['did'])
    prev_out_both_years_full_drivers = Y09_prev_out_did.intersection(Y10_prev_out_did)
    subset_drivers = general_both_years_full_drivers.intersection(prev_in_both_years_full_drivers)
    subset_drivers = list(subset_drivers.intersection(prev_out_both_years_full_drivers)) 
    #
    Y09_general = Y09_general[Y09_general['did'].isin(subset_drivers)]
    Y10_general = Y10_general[Y10_general['did'].isin(subset_drivers)]
    Y09_prev_in = Y09_prev_in[Y09_prev_in['did'].isin(subset_drivers)]
    Y10_prev_in = Y10_prev_in[Y10_prev_in['did'].isin(subset_drivers)]
    Y09_prev_out = Y09_prev_out[Y09_prev_out['did'].isin(subset_drivers)]
    Y10_prev_out = Y10_prev_out[Y10_prev_out['did'].isin(subset_drivers)]
    #
    Y09_general_gb, Y10_general_gb = Y09_general.groupby(['did']), Y10_general.groupby(['did'])
    Y09_driver_general_prod = Y09_general_gb.mean()['total-prod'].to_frame('avg_total_prod').reset_index()
    Y10_driver_general_prod = Y10_general_gb.mean()['total-prod'].to_frame('avg_total_prod').reset_index()
    Y09_driver_genprod_hour = {did : total_prod * HOUR / CENT for did, total_prod in Y09_driver_general_prod.values}
    Y10_driver_genprod_hour = {did : total_prod * HOUR / CENT for did, total_prod in Y10_driver_general_prod.values}
    #
    Y09_prev_in_gb, Y10_prev_in_gb = Y09_prev_in.groupby(['did']), Y10_prev_in.groupby(['did'])
    Y09_prev_in_driver_ap_prod = Y09_prev_in_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y10_prev_in_driver_ap_prod = Y10_prev_in_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y09_prev_in_driver_eco_pro = Y09_prev_in_gb.mean()['ap-eco-profit'].to_frame('avg_eco_pro').reset_index()
    Y10_prev_in_driver_eco_pro = Y10_prev_in_gb.mean()['ap-eco-profit'].to_frame('avg_eco_pro').reset_index()
    #
    Y09_pin_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y09_prev_in_driver_ap_prod.values}
    Y10_pin_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y10_prev_in_driver_ap_prod.values}
    Y09_pin_driver_epro_month = {did : eco_pro / CENT for did, eco_pro in Y09_prev_in_driver_eco_pro.values}
    Y10_pin_driver_epro_month = {did : eco_pro / CENT for did, eco_pro in Y10_prev_in_driver_eco_pro.values}
    #
    Y09_prev_out_gb, Y10_prev_out_gb = Y09_prev_out.groupby(['did']), Y10_prev_out.groupby(['did'])
    Y09_prev_out_driver_ap_prod = Y09_prev_out_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y10_prev_out_driver_ap_prod = Y10_prev_out_gb.mean()['ap-prod'].to_frame('avg_ap_prod').reset_index()
    Y09_prev_out_driver_eco_pro = Y09_prev_out_gb.mean()['ap-eco-profit'].to_frame('avg_eco_pro').reset_index()
    Y10_prev_out_driver_eco_pro = Y10_prev_out_gb.mean()['ap-eco-profit'].to_frame('avg_eco_pro').reset_index()
    #
    Y09_pout_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y09_prev_out_driver_ap_prod.values}
    Y10_pout_driver_aprod_hour = {did : ap_prod * HOUR / CENT for did, ap_prod in Y10_prev_out_driver_ap_prod.values}
    Y09_pout_driver_epro_month = {did : eco_pro / CENT for did, eco_pro in Y09_prev_out_driver_eco_pro.values}
    Y10_pout_driver_epro_month = {did : eco_pro / CENT for did, eco_pro in Y10_prev_out_driver_eco_pro.values}
    
    save_pickle_file('%s/productivities_ext.pkl' % (individual_detail_dir),
                     [subset_drivers,
                      Y09_driver_genprod_hour, Y10_driver_genprod_hour,
                      Y09_pin_driver_aprod_hour, Y10_pin_driver_aprod_hour,
                      Y09_pout_driver_aprod_hour, Y10_pout_driver_aprod_hour,
                      Y09_pin_driver_epro_month, Y10_pin_driver_epro_month,
                      Y09_pout_driver_epro_month, Y10_pout_driver_epro_month
                      ])

def test():
    def difference(data0, data1):
        diff = {}
        for k, v in data0.iteritems():
            diff[k] = data1[k] - v
        return diff
    def ordering(dids_values):
        order_v_did = []
        for did, v in dids_values.iteritems():
            order_v_did.append([v, did])
        order_v_did.sort()
        order_v_did.reverse()
        return order_v_did
    def find_extreme_range(order_v_did):
        # more than mean's 50 percent
        values = [v for v, _ in order_v_did]
        mu, std = np.mean(values), np.std(values)
        i = 0
        while order_v_did[i][0] > mu + std * 2.0:
            i += 1
        return (0, i / len(order_v_did))
    both_years_full_drivers, \
    Y09_driver_genprod_hour, Y10_driver_genprod_hour, \
    Y09_pin_driver_aprod_hour, Y10_pin_driver_aprod_hour, \
    Y09_pout_driver_aprod_hour, Y10_pout_driver_aprod_hour, \
    Y09_pin_driver_epro_month, Y10_pin_driver_epro_month, \
    Y09_pout_driver_epro_month, Y10_pout_driver_epro_month = load_picle_file('%s/productivities_ext.pkl' % (individual_detail_dir))
    #
    diff_general_prod = difference(Y09_driver_genprod_hour, Y10_driver_genprod_hour)
    diff_pin_prod = difference(Y09_pin_driver_aprod_hour, Y10_pin_driver_aprod_hour)
    diff_pout_prod = difference(Y09_pout_driver_aprod_hour, Y10_pout_driver_aprod_hour)
    diff_pin_eco = difference(Y09_pin_driver_epro_month, Y10_pin_driver_epro_month)
    diff_pout_eco = difference(Y09_pout_driver_epro_month, Y10_pout_driver_epro_month)
    
    order_v_did = ordering(diff_pin_eco)
    print len(diff_pin_eco)
    r1, r2 = find_extreme_range(order_v_did)
    extreme_drivers = [int(did) for _, did in order_v_did[int(r1 * len(order_v_did)):int(r2 * len(order_v_did))]]
    for fn in get_all_files(for_full_driver_dir, 'full-drivers-trips-', '.csv'):
        _, _, _, yymm = fn[:-len('.csv')].split('-')
        with open('%s/%s' % (for_full_driver_dir, fn), 'rb') as r_csvfile:
            reader = csv.reader(r_csvfile)
            headers = reader.next()
            id_did = headers.index('did')
            with open('%s/diff-pin-eco-extreme-drivers-trip-%s.csv' % (for_full_driver_dir, yymm), 'wt') as w_csvfile:
                writer = csv.writer(w_csvfile)
                writer.writerow(headers)
                for row in reader:
                    did = int(row[id_did])
                    if did not in extreme_drivers:
                        continue
                    writer.writerow(row)

if __name__ == '__main__':
    test()
#     run()
