#!/usr/bin/env python3

from distutils.core import setup, Extension
import os
import os.path
import re

use_cython = 1
if use_cython:
    from Cython.Distutils import build_ext
    ext_modules = [Extension("primitives",
        ["src/gensokyo/cython/primitives.pyx"])]
else:
    class build_ext: pass
    ext_modules = [Extension("primitives",
        ["src/gensokyo/cython/primitives.c"])]


def make_listing(dir):
    return (dir, [os.path.join(dir, x) for x in os.listdir(dir) if
        os.path.isfile(os.path.join(dir, x))])

def rmake(dir):
    l = []
    rmake_listing(dir, l)
    return l

def rmake_listing(dir, l):
    l.append(make_listing(dir))
    for d in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, d)):
            rmake_listing(os.path.join(dir, d), l)

p_py = re.compile(r'(.+)\.py')
def get_modules(dir):
    return [p_py.match(x).group(1) for x in os.listdir(dir) if p_py.match(x)]

setup(
    name = 'TouhouS',
    version='1.0',
    description='TouhouS game',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    package_dir={'':'src'},
    py_modules=get_modules('src'),
    cmdclass = {'build_ext': build_ext},
    ext_package = 'gensokyo',
    ext_modules = ext_modules,
    scripts=['bin/profile.py'],
    data_files=rmake('resources')
)
