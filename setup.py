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
        'gensokyo.player', 'gensokyo.stages', 'gensokyo.tests'],
    cmdclass = {'build_ext': build_ext},
    ext_package = 'gensokyo',
    ext_modules = ext_modules,
    data_files = [
        (data_dir + '', ['touhouS.py']),
        (data_dir + 'resources', [ 'resources/power.png', 'resources/star.png',
            'resources/icon16.png', 'resources/icon32.png',
            'resources/point.png', 'resources/ui.png',
            'resources/players/reimu/option.png',
            'resources/players/reimu/shot.png',
            'resources/players/reimu/hitbox.png',
            'resources/players/reimu/shot2.png',
            'resources/players/reimu/player.png',
            'resources/enemies/generic.png', 'resources/bullets/round.png' ])]
)
