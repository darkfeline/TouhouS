#!/usr/bin/env python3

import os
from distutils.core import setup, Extension

use_cython = 1


def get_resources(dir, l=None):
    if l is None:
        l = []
    l.append(_make_listing(dir))
    for d in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, d)):
            get_resources(os.path.join(dir, d), l)
    return l


def _make_listing(dir):
    return (dir, [os.path.join(dir, x) for x in os.listdir(dir) if
            os.path.isfile(os.path.join(dir, x))])

if use_cython:
    from Cython.Distutils import build_ext
    cmdclass = {'build_ext': build_ext}
    ext_modules = [Extension(
        "gensokyo.primitives", ["src/gensokyo/primitives.pyx"])]
else:
    cmdclass = {}
    ext_modules = [Extension(
        "gensokyo.primitives", ["src/gensokyo/primitives.c"])]

setup(
    name='TouhouS',
    version='1.0',
    description='TouhouS game',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    url='http://abagofapples.com/',
    package_dir={'': 'src'},
    packages=['gensokyo',
              'gensokyo.ces',
              'gensokyo.scene',
              'gensokyo.test'],
    ext_modules=ext_modules,
    cmdclass=cmdclass,
    scripts=['src/bin/touhouS'],
    data_files=get_resources('resources')
)
