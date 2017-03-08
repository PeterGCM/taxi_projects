from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import sys

args = sys.argv

if len(args) == len(['pyFile', 'packageName', 'fileName']):
    _, packageName, fileName = args

    ext_modules = [
        Extension('%s.%s' % (packageName, fileName),
                  ['%s/%s.pyx' % (packageName, fileName)], include_dirs=['.']),
    ]

    setup(
        name='taxi_projects',
        cmdclass={'build_ext': build_ext},
        ext_modules=ext_modules,
        script_args=['build_ext'],
        options={'build_ext': {'inplace': True, 'force': True}}
    )

    print '******** CYTHON COMPLETE ******'
else:
    print '******** Error ******'
    print '******** Type packageName and fileName ******'