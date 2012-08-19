#!/usr/bin/env python3

from distutils.core import setup, Extension

use_cython = 1
if use_cython:
    from Cython.Distutils import build_ext
    ext_modules = [Extension("rect", ["gensokyo/cython/rect.pyx"])]
else:
    ext_modules = [Extension("rect", ["gensokyo/cython/rect.c"])]

setup(
    name = 'Gensokyo',
    version='1.0',
    description='TouhouS game engine',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    packages=['gensokyo', 'gensokyo.bullet', 'gensokyo.enemy',
        'gensokyo.player', 'gensokyo.stages', 'gensokyo.tests'],
    cmdclass = {'build_ext': build_ext},
    ext_package = 'gensokyo',
    ext_modules = ext_modules,
    scripts = ['touhouS.py'],
    package_data = {'gensokyo':['resources/*.png', 'resources/bullets/*.png',
        'resources/enemies/*.png', 'resources/players/*.png']}
)
