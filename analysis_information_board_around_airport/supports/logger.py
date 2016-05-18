from __future__ import division
#
import os, __main__
from time import strftime
#
log_fn = 'log.txt'

if not os.path.exists(log_fn):
    with open(log_fn, 'w') as f:
        f.write(strftime("%a, %d %b %Y %H:%M:%S---") + 'Start logging' + '\n')

def logging_msg(msg):
    with open(log_fn, 'a') as f:
        f.write(strftime("%a, %d %b %Y %H:%M:%S---") + msg + '   %s' % (__main__.__file__) + '\n')
            
if __name__ == '__main__':
    logging_msg('test')
