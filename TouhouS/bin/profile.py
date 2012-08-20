#!/usr/bin/env python3

import pstats, cProfile

import pyximport
pyximport.install()

import touhouS

cProfile.runctx("touhouS.main()", globals(), locals(), "Profile.prof")

s = pstats.Stats("Profile.prof")
s.strip_dirs().sort_stats("time").print_stats()
