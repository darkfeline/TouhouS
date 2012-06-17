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
        self._high_score = 0
        self._score = 0
        self._lives = 3
        self._bombs = 3
        self.label = {}
        self.label['high_score'] = UILabel(y=415, text='High score {}'.format(
            self._high_score))
        self.label['score'] = UILabel(y=391, text='Score {}'.format(
            self._score))
        self.label['lives'] = UILabel(y=361, text='Lives {}'.format(
            self._lives))
        self.label['bombs'] = UILabel(y=339, text='Bombs {}'.format(
            self._bombs))

    @property
    def high_score(self):
        return self._high_score

    @high_score.setter
    def high_score(self, value):
        self._high_score = value

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value

    @property
    def bombs(self):
        return self._bombs

    @bombs.setter
    def bombs(self, value):
        self._bombs = value

    def on_draw(self):
        self.draw()

    def update(self, dt):
        pass

    def draw(self):
        self.bg.blit(0, 0)
        for k in self.label.keys():
            self.label[k].draw()
        self.fps.draw()
