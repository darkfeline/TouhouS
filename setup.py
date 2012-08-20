#!/usr/bin/env python3

from distutils.core import setup, Extension

try:
    from Cython.Distutils import build_ext
except ImportError:
    class build_ext:
        pass

use_cython = 1
if use_cython:
    ext_modules = [Extension("rect", ["gensokyo/cython/rect.pyx"]),
            Extension("collision", ["gensokyo/cython/collision.pyx"])]
else:
    ext_modules = [Extension("rect", ["gensokyo/cython/rect.c"]),
            Extension("collision", ["gensokyo/cython/collision.c'"])]

data_dir = ''

setup(
    name = 'Gensokyo',
    version='1.0',
    description='TouhouS game engine',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    packages=['gensokyo', 'gensokyo.bullet', 'gensokyo.enemy',
        'gensokyo.player', 'gensokyo.stages', 'gensokyo.tests',
        'gensokyo.data'],
    cmdclass = {'build_ext': build_ext},
    ext_package = 'gensokyo',
    ext_modules = ext_modules,
    package_data = {'gensokyo': ['data/*.png', 'data/enemies/*.png',
        'data/players/reimu/*.png', 'data/bullets/*.png']},
    data_files = [('', ['touhouS.py', 'bin/profile.py'])]
)
