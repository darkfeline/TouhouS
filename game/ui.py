#!/usr/bin/env python3

from pyglet.clock import ClockDisplay

from game import resources

class FPSDisplay(ClockDisplay):
    pass

class UI:

    def __init__(self):
        self.bg = resources.ui_image

    def on_draw(self):
        self.draw()

    def update(self, dt):
        pass

    def draw(self):
        self.bg.blit(0, 0)
