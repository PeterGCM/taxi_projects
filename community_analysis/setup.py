from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("b_group._cy_b3b_XgroupTripsShifts", ["b_group/_cy_b3b_XgroupTripsShifts.pyx"], include_dirs=['.']),
    # Extension("a_preprocessing._cy_a3_time_pickUp", ["a_preprocessing/_cy_a3_time_pickUp.pyx"], include_dirs=['.']),
]

setup(
    name='taxi_projects',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    script_args=['build_ext'],
    options={'build_ext': {'inplace': True, 'force': True}}
)

print '********CYTHON COMPLETE******'