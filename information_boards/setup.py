# Use this setup.py if you want to specify each extension module by hand
# To run this setup do exefile('pathToThisSetup.py')

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# All module name should be fully qualified
# All path should be fully qualified starting at the codeRootFolder
# your include_dirs must contains the '.' for setup to search all the subfolder of the codeRootFolder
ext_modules = [
    Extension("b_report.helloworld", ["b_report/helloworld.pyx"], include_dirs=['.']),
    # Extension("codeRootFolder.cythonAnimal.dog", ["codeRootFolder/cythonAnimal/dog.pyx"], include_dirs=['.'])
]

setup(
    name='workingCythonMultiPackageProject',
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    script_args=['build_ext'],
    options={'build_ext': {'inplace': True, 'force': True}}
)

print '********CYTHON COMPLETE******'