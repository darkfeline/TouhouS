#!/usr/bin/env python3

from distutils.core import setup, Extension
import os
import os.path

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

setup(
    name = 'TouhouS',
    version='1.0',
    description='TouhouS game',
    author='Allen Li',
    author_email='darkfeline@abagofapples.com',
    package_dir={'':'src'},
    py_modules=['touhouS', 'reimu', 'enemy', 'stage', 'model', 'resources'],
    packages=[],
    scripts=['bin/profile.py'],
    data_files=rmake('resources')
)
