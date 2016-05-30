from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import summary_dir
from supports.etc_functions import check_dir_create, remove_file
from supports._setting import Y09_ftd_general_stat, Y10_ftd_general_stat
from supports._setting import Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat
from supports._setting import Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat
from supports._setting import Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat
from supports._setting import Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat
from supports._setting import SEC3600, CENT
from supports.etc_functions import save_pickle_file
#
from supports._setting import ftd_general_prod_db, ftd_ap_prod_eco_prof_db, ftd_ns_prod_eco_prof_db
#
import pandas as pd
#
_package = [Y09_ftd_general_stat, Y10_ftd_general_stat,
            Y09_ftd_prev_in_ap_stat, Y10_ftd_prev_in_ap_stat,
            Y09_ftd_prev_in_ns_stat, Y10_ftd_prev_in_ns_stat,
            Y09_ftd_prev_out_ap_stat, Y10_ftd_prev_out_ap_stat,
            Y09_ftd_prev_out_ns_stat, Y10_ftd_prev_out_ns_stat]
dfs = [pd.read_csv(path_fn) for path_fn in _package]
#
Y09_GEN, Y10_GEN, \
Y09_PIAP, Y10_PIAP, \
Y09_POAP, Y10_POAP, \
Y09_PINS, Y10_PINS, \
Y09_PONS, Y10_PONS = range(10)
 
def run():
    check_dir_create(summary_dir)
    for path in [ftd_general_prod_db, ftd_ap_prod_eco_prof_db, ftd_ns_prod_eco_prof_db]:
        remove_file(path)
    #
    save_pickle_file(ftd_general_prod_db , general_productivities())
    save_pickle_file(ftd_ap_prod_eco_prof_db, ap_productivities_economical_profits())
    save_pickle_file(ftd_ns_prod_eco_prof_db, ns_productivities_economical_profits())

def general_productivities():
    drivers_hourly_producities = []
    for i in [Y09_GEN, Y10_GEN]:
        df_gb = dfs[i].groupby(['did'])
        drivers_avg_productivities = df_gb.mean()['total-prod'].to_frame('avg_total_prod').reset_index()
        drivers_hourly_producities.append(
                  {did : total_prod * SEC3600 / CENT for did, total_prod in drivers_avg_productivities.values})
    return drivers_hourly_producities 

def ap_productivities_economical_profits():
    #
    # drivers who operate taxi in both years
    #
    ap_full_drivers = set(dfs[Y09_PIAP]['did'])
    for i in [Y10_PIAP, Y09_POAP, Y10_POAP]:
        ap_full_drivers = ap_full_drivers.intersection(set(dfs[i]['did']))
    #
    return get_driver_average(ap_full_drivers, [Y09_PIAP, Y10_PIAP, Y09_POAP, Y10_POAP])
    
def ns_productivities_economical_profits():
    #
    # drivers who operate taxi in both years
    #
    ns_full_drivers = set(dfs[Y09_PINS]['did'])
    for i in [Y10_PINS, Y09_PONS, Y10_PONS]:
        ns_full_drivers = ns_full_drivers.intersection(set(dfs[i]['did']))
    #
    return get_driver_average(ns_full_drivers, [Y09_PINS, Y10_PINS, Y09_PONS, Y10_PONS])

def get_driver_average(full_drivers, df_indices):
    #
    # filter our part-time drivers
    #   and save each drivers' productivities and economical profits
    #
    drivers_ap_prod_eco_prof = []
    for i in df_indices:
        df = dfs[i] 
        df = df[df['did'].isin(full_drivers)]
        gb_df = df.groupby(['did'])
        drivers_ap_prod = gb_df.mean()['prod'].to_frame('avg_prod').reset_index()
        drivers_ap_prod_hour = {did : ap_prod * SEC3600 / CENT for did, ap_prod in drivers_ap_prod.values}
        #
        drivers_eco_prof = gb_df.mean()['eco-profit'].to_frame('avg_eco_pro').reset_index()
        drivers_eco_prof_month = {did : eco_pro / CENT for did, eco_pro in drivers_eco_prof.values}
        #
        drivers_ap_prod_eco_prof.append([drivers_ap_prod_hour, drivers_eco_prof_month])
    return drivers_ap_prod_eco_prof

if __name__ == '__main__':
    run()
