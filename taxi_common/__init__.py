import os, sys, platform
from os.path import expanduser
#
user_home = expanduser("~")
taxi_home = None
#
# Check environments and set a prefix for finding files and libraries
#
py_vinfo = sys.version_info
if type(sys.version_info) == type(()):
    print 'This python is not 2.7 version'
    assert False
if py_vinfo.major == 2 and py_vinfo.minor == 7:
    plf = platform.platform()
    if plf.startswith('Linux'):
        # Linux server
        sys.path.append(user_home + '/local/lib/python2.7/site-packages')
        sys.path.append(user_home + '/local/lib64/python2.7/site-packages')
        taxi_home = user_home + '/../taxi'
    elif plf.startswith('Darwin'):
        # Mac
        pass
    else:
        # Window ?
        pass
    sys.path.append(os.getcwd() + '/..')
#     sys.path.append(os.getcwd() + '/../taxi_common/test')
else:
    print 'This python is not 2.7 version'
    assert False
#
tc_data = os.path.dirname(os.path.realpath(__file__)) + '/data_20160826'
singapore_poly_fn = tc_data + '/Singapore_polygon'
singapore_grid_xy_points = tc_data + '/Singapore_grid_xy_points.pkl'
singapore_zones = tc_data + '/Singapore_zones.pkl'

ZONE_UNIT_KM = 0.5
METER1000 = 1000


def get_taxi_home_path():
    return taxi_home