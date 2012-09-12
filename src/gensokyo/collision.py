#!/usr/bin/env python3

import weakref

from pyglet.event import EventDispatcher

class CollisionManager(EventDispatcher):

    def __init__(self):
        self.components = []

    def add(self, component, type, method):
        self.components.append((weakref.ref(component), type, method))

    def update(self, dt):
        items = self.components[:]
        for ac, at, am in items:
            for bc, bt, bm in items:
                if a.collide(b):
                    if isinstance(bc, at) and af is not None:
                        af(a)
                    if isinstance(ac, bt) and bf is not None:
                        bf(b)
