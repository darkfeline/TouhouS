#!/usr/bin/env python3

import os
import sys
from distutils.core import setup, Extension


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


def pack_ext(extensions, cython):
    return [Extension(
        x, [os.path.join('src', *x.split('.')) + ('.pyx' if cython else '.c')]
    ) for x in extensions]

extensions = ['gensokyo.primitives']
if sys.argv[1] == 'c':
    del sys.argv[1]
    from Cython.Distutils import build_ext
    cmdclass = {'build_ext': build_ext}
    ext_modules = pack_ext(extensions, True)
else:
    cmdclass = {}
    ext_modules = pack_ext(extensions, False)

setup(
    name='TouhouS',
    version='0.1',
    description='TouhouS game',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    requires=['pyglet'],
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
