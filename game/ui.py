#!/usr/bin/env python3

from pyglet.clock import ClockDisplay
from pyglet.text import Label

from game import resources

class FPSDisplay(ClockDisplay):
    pass


class UILabel(Label):

    def __init__(self, anchor_x='left', anchor_y='bottom', font_size=10, x=420,
            width=190, *args, **kwargs):
        super().__init__(*args, x=x, width=width, anchor_x=anchor_x, anchor_y=anchor_y,
                font_size=font_size, **kwargs)


class UI:

    def __init__(self):
        self.bg = resources.ui_image
        self.fps = FPSDisplay()

    def on_draw(self):
        self.draw()

    def update(self, dt):
        pass

    def draw(self):
        self.bg.blit(0, 0)
        self.fps.draw()
