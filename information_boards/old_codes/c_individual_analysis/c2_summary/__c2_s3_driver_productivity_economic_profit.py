import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import SEC3600, CENT
from c_individual_analysis.__init__ import ftd_gen_prod_db_for_ap, ftd_ap_prod_eco_prof_db
from c_individual_analysis.__init__ import ftd_gen_prod_db_for_ns, ftd_ns_prod_eco_prof_db
from __init__ import dfs
from __init__ import Y09_GEN, Y10_GEN, Y09_PIAP, Y10_PIAP, Y09_POAP, Y10_POAP, Y09_PINS, Y10_PINS, Y09_PONS, Y10_PONS
#
from taxi_common.file_handling_functions import remove_file, save_pickle_file
#
def run():
    for path in [ftd_gen_prod_db_for_ap, ftd_gen_prod_db_for_ns, ftd_ap_prod_eco_prof_db, ftd_ns_prod_eco_prof_db]:
        remove_file(path)
    #
    ap_productivity_economical_profit()
    ns_productivity_economical_profit()

def general_productivities(full_drivers):
    drivers_hourly_producities = []
    for i in [Y09_GEN, Y10_GEN]:
        df = dfs[i]
        df = df[((df['prod'] - df['prod'].mean()) / df['prod'].std()).abs() < 3]
        df = df[df['did'].isin(full_drivers)]
        df_gb = df.groupby(['did'])
        drivers_avg_productivities = df_gb.mean()['prod'].to_frame('avg_prod').reset_index()
        drivers_hourly_producities.append(
                  {did : total_prod * SEC3600 / CENT for did, total_prod in drivers_avg_productivities.values})
    return drivers_hourly_producities 

def ap_productivity_economical_profit():
    #
    # drivers who operate taxi in both years
    #
    df = dfs[Y09_PIAP]
    df = df[((df['prod'] - df['prod'].mean()) / df['prod'].std()).abs() < 3]
    df = df[((df['eco-profit'] - df['eco-profit'].mean()) / df['eco-profit'].std()).abs() < 3]
    ap_full_drivers = set(df['did'])
    for i in [Y10_PIAP, Y09_POAP, Y10_POAP]:
        df = dfs[i]
        df = df[((df['prod'] - df['prod'].mean()) / df['prod'].std()).abs() < 3]
        df = df[((df['eco-profit'] - df['eco-profit'].mean()) / df['eco-profit'].std()).abs() < 3]
        ap_full_drivers = ap_full_drivers.intersection(set(df['did']))
    #
    save_pickle_file(ftd_gen_prod_db_for_ap, general_productivities(ap_full_drivers))
    save_pickle_file(ftd_ap_prod_eco_prof_db, get_driver_average(ap_full_drivers, [Y09_PIAP, Y10_PIAP, Y09_POAP, Y10_POAP]))

def ns_productivity_economical_profit():
    #
    # drivers who operate taxi in both years
    #
    df = dfs[Y09_PINS]
    df = df[((df['prod'] - df['prod'].mean()) / df['prod'].std()).abs() < 3]
    df = df[((df['eco-profit'] - df['eco-profit'].mean()) / df['eco-profit'].std()).abs() < 3]
    ns_full_drivers = set(df['did'])
    for i in [Y10_PINS, Y09_PONS, Y10_PONS]:
        df = dfs[i]
        df = df[((df['prod'] - df['prod'].mean()) / df['prod'].std()).abs() < 3]
        df = df[((df['eco-profit'] - df['eco-profit'].mean()) / df['eco-profit'].std()).abs() < 3]
        ns_full_drivers = ns_full_drivers.intersection(set(df['did']))
    #
    save_pickle_file(ftd_gen_prod_db_for_ns, general_productivities(ns_full_drivers))
    save_pickle_file(ftd_ns_prod_eco_prof_db, get_driver_average(ns_full_drivers, [Y09_PINS, Y10_PINS, Y09_PONS, Y10_PONS]))

def get_driver_average(full_drivers, df_indices):
    #
    # filter our part-time drivers
    #   and save each drivers' productivities and economical profits
    #
    drivers_prod_eco_prof = []
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
        drivers_prod_eco_prof.append([drivers_ap_prod_hour, drivers_eco_prof_month])
    return drivers_prod_eco_prof

if __name__ == '__main__':
    run()
