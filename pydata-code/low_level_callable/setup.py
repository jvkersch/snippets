from distutils.core import setup
from Cython.Build import cythonize

import numpy


setup(
    name='callable',
    ext_modules=cythonize('callable.pyx'),
    include_dirs=[numpy.get_include()],
)
