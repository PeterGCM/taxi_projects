from __future__ import division
# 
import os, sys  
sys.path.append(os.getcwd() + '/..')
#
from supports.etc_functions import get_all_files
from supports._setting import airport_trips_dir, op_cost_summary
from supports._setting import Q_LIMIT_MIN, Q_LIMIT_MAX
from supports.logger import logging_msg
from supports.multiprocess import init_multiprocessor, put_task, end_multiprocessor
#
import csv, datetime, time
from traceback import format_exc
#
