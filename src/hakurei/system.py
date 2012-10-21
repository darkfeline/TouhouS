#!/usr/bin/env python3

from pyglet import clock

from gensokyo import ces

from hakurei import component


class FPSSystem(ces.System):

    def __init__(self):
        self.count = 0

    def update(self, dt):
        self.count += dt
        if self.count > 1:
            entity = self.get_tag('fps_display')
            for l in entity.get(component.Label):
                l.label.text = "{0:.1f}".format(clock.get_fps()) + ' fps'
            self.count = 0
