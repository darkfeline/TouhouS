#!/usr/bin/env python

from distutils.core import setup, Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("rect", ["rect.pyx"])]

setup(
  name = 'Extension modules',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)
