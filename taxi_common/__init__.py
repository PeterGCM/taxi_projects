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
shifts_dir, shift_prefix = '/home/sfcheng/toolbox/results', 'shift-hour-state-'
#
ZONE_UNIT_KM = 0.5
#
tc_data = os.path.dirname(os.path.realpath(__file__)) + '/data'
sg_poly_fpath = '%s/%s' % (tc_data, 'Singapore_polygon')
sg_grid_xy_points = tc_data + '/sg_grid_xy_points(%.1fkm).pkl' % ZONE_UNIT_KM
sg_zones = tc_data + '/sg_zones(%.1fkm).pkl' % ZONE_UNIT_KM
full_time_driver_dir, ft_drivers_prefix = '%s/%s' % (tc_data, 'full_time_drivers_by_shift'), 'ft-drivers-'
dl_by_trip_dir, dl_by_trip_prefix = '%s/%s' % (tc_data, 'drivers_by_trips'), 'drivers-'
#


def get_taxi_home_path():
    return taxi_home