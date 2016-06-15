from __future__ import division
#
import os, sys
sys.path.append(os.getcwd() + '/../..')
#
from supports._setting import ftd_general_prod_mb, ftd_ap_prod_eco_prof_mb, ftd_ns_prod_eco_prof_mb
from supports._setting import tables_dir, ftd_overall_analysis
from supports.etc_functions import check_dir_create, load_picle_file, write_text_file
from supports.charts import x_twin_chart
#
import numpy as np
import scipy.stats as stats
from prettytable import PrettyTable

mean_t_test = lambda l1, l2: ("{:.2f}".format(np.mean(l1)), "{:.2f}".format(np.mean(l2)),
                              "{:.2f}".format(np.mean([l2[i] - l1[i] for i in xrange(len(l2))])),
                              "{:.2f}".format(np.std([l2[i] - l1[i] for i in xrange(len(l2))])),
                              "{:.2e}".format(stats.ttest_ind(l1, l2)[1]))

def run():
    check_dir_create(tables_dir)
    write_text_file(ftd_overall_analysis, 'Init', True)
    #
    # Load data
    #
    y09_gen_m_prod, y10_gen_m_prod = load_picle_file(ftd_general_prod_mb)
    (y09_piap_m_prod, y09_piap_m_eco_prof), \
    (y10_piap_m_prod, y10_piap_m_eco_prof), \
    (y09_poap_m_prod, y09_poap_m_eco_prof), \
    (y10_poap_m_prod, y10_poap_m_eco_prof) = load_picle_file(ftd_ap_prod_eco_prof_mb)
    (y09_pins_m_prod, y09_pins_m_eco_prof), \
    (y10_pins_m_prod, y10_pins_m_eco_prof), \
    (y09_pons_m_prod, y09_pons_m_eco_prof), \
    (y10_pons_m_prod, y10_pons_m_eco_prof) = load_picle_file(ftd_ns_prod_eco_prof_mb)
    #
    my_d = {
             # (Measure, Year): data
             ('General prod.', 'Y09'): y09_gen_m_prod,
             ('General prod.', 'Y10'): y10_gen_m_prod,
             #
             ('AP in prod.'  , 'Y09'): y09_piap_m_prod,
             ('AP in prod.'  , 'Y10'): y10_piap_m_prod,
             ('AP out prod.' , 'Y09'): y09_poap_m_prod,
             ('AP out prod.' , 'Y10'): y10_poap_m_prod,
             ('AP in eco.'   , 'Y09'): y09_piap_m_eco_prof,
             ('AP in eco.'   , 'Y10'): y10_piap_m_eco_prof,
             ('AP out eco.'  , 'Y09'): y09_poap_m_eco_prof,
             ('AP out eco.'  , 'Y10'): y10_poap_m_eco_prof,
             #
             ('NS in prod.'  , 'Y09'): y09_pins_m_prod,
             ('NS in prod.'  , 'Y10'): y10_pins_m_prod,
             ('NS out prod.' , 'Y09'): y09_pons_m_prod,
             ('NS out prod.' , 'Y10'): y10_pons_m_prod,
             ('NS in eco.'   , 'Y09'): y09_pins_m_eco_prof,
             ('NS in eco.'   , 'Y10'): y10_pins_m_eco_prof,
             ('NS out eco.'  , 'Y09'): y09_pons_m_eco_prof,
             ('NS out eco.'  , 'Y10'): y10_pons_m_eco_prof,
             }
    #
    both_year_comparison(my_d)
    draw_month_change(my_d)
    
def both_year_comparison(my_d):
    def init_table():
        _table = PrettyTable(["Measeure", "Y2009", "Y2010", "Diff.", "S.D", "t-test (p-value)"])
        _table.align["Measeure"] = "l"
        return _table
    #
    # General trips
    #
    gen_table = init_table()
    measure = 'General prod.'
    arg1, arg2, arg3, arg4, arg5 = \
                    mean_t_test(my_d[(measure, 'Y09')], my_d[(measure, 'Y10')])
    gen_table.add_row([measure, arg1, arg2, arg3, arg4, arg5])
    write_text_file(ftd_overall_analysis, gen_table.get_string())
    #
    # Aiport trips
    #
    ap_table = init_table()
    for measure in ['AP in prod.', 'AP out prod.', 'AP in eco.', 'AP out eco.']:
        arg1, arg2, arg3, arg4, arg5 = \
                        mean_t_test(my_d[(measure, 'Y09')], my_d[(measure, 'Y10')])
        ap_table.add_row([measure, arg1, arg2, arg3, arg4, arg5])
    write_text_file(ftd_overall_analysis, ap_table.get_string())
    #
    # Night safari trips
    #
    ns_table = init_table()
    for measure in ['NS in prod.', 'NS out prod.', 'NS in eco.', 'NS out eco.']:
        arg1, arg2, arg3, arg4, arg5 = \
                        mean_t_test(my_d[(measure, 'Y09')], my_d[(measure, 'Y10')])
        ns_table.add_row([measure, arg1, arg2, arg3, arg4, arg5])
    write_text_file(ftd_overall_analysis, ns_table.get_string())

def draw_month_change(my_d): 
    months = ['0901', '0902', '0903', '0904', '0905', '0906', '0907', '0908', '0909', '0910', '0911',
              '1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008', '1009', '1011', '1012']
    measure = 'General prod.'
    for LOC in ['AP', 'NS']:
        measure = 'General prod.'
        productivities = [my_d[(measure, 'Y09')] + my_d[(measure, 'Y10')]]
        for measure in ['%s in prod.' % LOC, '%s out prod.' % LOC]:
            productivities.append([])
            productivities[-1] += my_d[(measure, 'Y09')] + my_d[(measure, 'Y10')] 
        eco_profits = []
        for measure in ['%s in eco.' % LOC, '%s out eco.' % LOC]:
            eco_profits.append([])
            eco_profits[-1] += my_d[(measure, 'Y09')] + my_d[(measure, 'Y10')]
        if LOC == 'AP':
            y_info1_lb, y_info1_ub = 15, 32
            y_info2_lb, y_info2_ub = 250, -150
        else:
            y_info1_lb, y_info1_ub = 15, 32
            y_info2_lb, y_info2_ub = 250, -250
        x_info = ('Year and Month', months, 15)
        y_info1 = ('$S/Hour', productivities, (y_info1_lb, y_info1_ub), 
                   ['General productivity', 'Prev. in %s productivity' % LOC, 'Prev. out %s productivity' % LOC], 'upper left')
        y_info2 = ('$/Month', eco_profits, (y_info2_lb, y_info2_ub), 
                   ['Prev. in %s economic profit.' % LOC, 'Prev. out %s economic profit' % LOC], 'upper right') 
        loc = 'ap' if LOC == 'AP' else 'ns'
        x_twin_chart((12, 6), '', x_info, y_info1, y_info2, 'productivities_economic_profits_%s' % loc)

if __name__ == '__main__':
    run()
