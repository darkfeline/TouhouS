#!/usr/bin/env python3

from gensokyo import ces


class Wrapper(ces.Entity):

    def __init__(self, component):
        self.add(component)
