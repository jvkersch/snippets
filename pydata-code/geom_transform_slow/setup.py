from distutils.core import setup, Extension
import numpy

shift = Extension('example',
                  ['example.c'],
                  include_dirs=[numpy.get_include()]
)

setup(name='example',
      ext_modules=[shift]
)
