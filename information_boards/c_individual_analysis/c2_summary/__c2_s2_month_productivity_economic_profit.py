import __init__  # @UnresolvedImport # @UnusedImport
#
from __init__ import SEC3600, CENT
from c_individual_analysis.__init__ import ftd_general_prod_mb, ftd_ap_prod_eco_prof_mb, ftd_ns_prod_eco_prof_mb
from __init__ import dfs
from __init__ import Y09_GEN, Y10_GEN, Y09_PIAP, Y10_PIAP, Y09_POAP, Y10_POAP, Y09_PINS, Y10_PINS, Y09_PONS, Y10_PONS
#
from taxi_common.file_handling_functions import remove_file, save_pickle_file
#
def run():
    for path in [ftd_general_prod_mb, ftd_ap_prod_eco_prof_mb, ftd_ns_prod_eco_prof_mb]:
        remove_file(path)
    #
    save_pickle_file(ftd_general_prod_mb , general_productivity())
    save_pickle_file(ftd_ap_prod_eco_prof_mb, ap_productivity_economical_profit())
    save_pickle_file(ftd_ns_prod_eco_prof_mb, ns_productivity_economical_profit())
    
def general_productivity():
    drivers_month_productivity = []
    for i in [Y09_GEN, Y10_GEN]:
        df = dfs[i]
        df = df[((df['prod'] - df['prod'].mean()) / df['prod'].std()).abs() < 3]
        df_gb = df.groupby(['mm'])
        prod_sec_mb = df_gb.mean()['prod'].to_frame('avg_prod').reset_index()
        drivers_month_productivity.append([prod * SEC3600 / CENT for _, prod in prod_sec_mb.values])
    return drivers_month_productivity

def ap_productivity_economical_profit():
    #
    # drivers who operate taxi in both years
    #
    ap_full_drivers = set(dfs[Y09_PIAP]['did'])
    for i in [Y10_PIAP, Y09_POAP, Y10_POAP]:
        ap_full_drivers = ap_full_drivers.intersection(set(dfs[i]['did']))
    return get_month_average(ap_full_drivers, [Y09_PIAP, Y10_PIAP, Y09_POAP, Y10_POAP])

def ns_productivity_economical_profit():
    #
    # drivers who operate taxi in both years
    #
    ns_full_drivers = set(dfs[Y09_PINS]['did'])
    for i in [Y10_PINS, Y09_PONS, Y10_PONS]:
        ns_full_drivers = ns_full_drivers.intersection(set(dfs[i]['did']))
    return get_month_average(ns_full_drivers, [Y09_PINS, Y10_PINS, Y09_PONS, Y10_PONS])

def get_month_average(full_drivers, df_indices):
    #
    # filter our part-time drivers
    #   and save each drivers' productivities and economical profits
    #
    month_prod_eco_prof = []
    for i in df_indices:
        df = dfs[i] 
        df = df[df['did'].isin(full_drivers)]
        df = df[((df['prod'] - df['prod'].mean()) / df['prod'].std()).abs() < 3]
        df = df[((df['eco-profit'] - df['eco-profit'].mean()) / df['eco-profit'].std()).abs() < 3]
        gb_df = df.groupby(['mm'])
        prod_sec_mb = gb_df.mean()['prod'].to_frame('avg_prod').reset_index()
        eco_prof_cent_mb = gb_df.mean()['eco-profit'].to_frame('avg_eco_pro').reset_index()
        month_prod_eco_prof.append([[prod * SEC3600 / CENT for _, prod in prod_sec_mb.values], 
                                    [eco_pro / CENT for _, eco_pro in eco_prof_cent_mb.values]])
    return month_prod_eco_prof

if __name__ == '__main__':
    run()
