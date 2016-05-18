from __future__ import division
# Add the root path for packages I made
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports._setting import for_learning_dir
from supports.etc_functions import get_all_files
#
for i in xrange(11):
    for j in xrange(11):
        ALPHA, GAMMA = i / 10, j / 10 
        dn = for_learning_dir + '/ALPHA-%.2f-GAMMA-%.2f' % (ALPHA, GAMMA)
        print ALPHA, GAMMA, 
        if not os.path.exists(dn):
            print 'None'
            continue
        print len(get_all_files(dn, 'ALPHA-', '.pkl')), 
        print len(get_all_files(dn, 'results-', '.pkl'))
        
