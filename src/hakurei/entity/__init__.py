#!/usr/bin/env python3

from gensokyo.entity import Entity


class DataEntity(Entity):

    def __init__(self, component):
        self.add(component)
