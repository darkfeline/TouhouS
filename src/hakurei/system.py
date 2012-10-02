#!/usr/bin/env python3

from pyglet import clock

from gensokyo.system import System
from gensokyo import component
from gensokyo import locator


class FPSSystem(System):

    def __init__(self):
        self.count = 0

    def update(self, dt):
        self.count += dt
        if self.count > 1:
            entity = locator.model.tm['fps_display']
            labels = entity.get((component.Label,))[0]
            for l in labels:
                l.label.text = "{0:.1f}".format(clock.get_fps()) + ' fps'
            self.count = 0
