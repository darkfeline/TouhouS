#!/usr/bin/env python3

from distutils.core import setup, Extension

from setup_utils import get_packages
from setup_utils import get_resources
from setup_utils import get_scripts


use_cython = 1
if use_cython:
    from Cython.Distutils import build_ext
    ext_modules = [Extension("gensokyo.primitives",
                             ["src/gensokyo/primitives.pyx"])]
else:
    class build_ext: pass
    ext_modules = [Extension("gensokyo.primitives",
                             ["src/gensokyo/primitives.c"])]

setup(
    name='TouhouS',
    version='1.0',
    description='TouhouS game',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    package_dir={'': 'src'},
    packages=get_packages('src'),
    cmdclass={'build_ext': build_ext},
    ext_modules=ext_modules,
    scripts=get_scripts('src/bin'),
    data_files=get_resources('resources')
)
