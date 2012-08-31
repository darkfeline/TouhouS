#!/usr/bin/env python3

import pyglet
from pyglet import text

from gensokyo.sprite import Sprite

class FPSDisplay:

    def __init__(self, x, y, batch):
        self._label = text.Label(x=x, y=y, anchor_x='left', anchor_y='bottom',
                font_size=10, color=(255, 255, 255, 255), batch=batch)
        self.count = 0

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        self._fps = value
        self._label.text = "{0:.1f}".format(self._fps) + 'fps'

    def update(self, dt):
        self.count += dt
        if self.count > 1:
            self.fps = pyglet.clock.get_fps()
            self.count -= 1


class Label:

    def __init__(self, x, y, title, number=0, width=190, batch=None):
        self._title = text.Label(anchor_x='left', anchor_y='bottom', font_size=10,
                color=(0, 0, 0, 255), batch=batch)
        self._number = text.Label(anchor_x='right', anchor_y='bottom', font_size=10,
                color=(0, 0, 0, 255), batch=batch)
        self.width = width
        self.x = x
        self.y = y
        self.title = title
        self.number = number

    @property
    def x(self):
        return self._title.x

    @x.setter
    def x(self, value):
        self._title.x = value
        self._number.x = self.width + value

    @property
    def y(self):
        return self._title.y

    @y.setter
    def y(self, value):
        self._title.y = value
        self._number.y = value

    @property
    def title(self):
        return self._title.text

    @title.setter
    def title(self, value):
        self._title.text = value

    @property
    def number(self):
        return self._number.text

    @number.setter
    def number(self, value):
        self._number.text = str(value)


class IconLabel(Label):

    def __init__(self, x, y, title, number=0, width=190, img=None,
            batch=None):
        self._title = text.Label(anchor_x='left', anchor_y='bottom',
                font_size=10, color=(0, 0, 0, 255), batch=batch)
        self.title = title
        self.width = width
        self.img = img
        self.icons = ()
        self.display_max = 8
        self.icon_width = self.icons[0].width
        self.number = number
        self.x = x
        self.y = y
        self.batch = batch

    @property
    def display_max(self):
        return self._display_max

    @display_max.setter
    def display_max(self, value):
        self._display_max = value
        self.icons = tuple([Sprite(img=self.img) for i in
            range(self._display_max)])

    @property
    def x(self):
        return self._title.x

    @x.setter
    def x(self, value):
        self._title.x = value
        start = value + self.width - self.display_max * self.icon_width
        for n, a in enumerate(self.icons):
            a.x = start + n * self.icon_width

    @property
    def y(self):
        return self._title.y

    @y.setter
    def y(self, value):
        self._title.y = value
        for i in self.icons:
            i.y = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        self._number = value
        i = -1
        for i in range(min(self.number, self.display_max)):
            self.icons[i].batch = self.batch
        i += 1
        while i < self.display_max:
            self.icons[i].batch = None
            i += 1


class UI:

    def __init__(self, bg=None, icon=None):
        self.bg = bg
        self.batch = pyglet.graphics.Batch()
        self.fps = FPSDisplay(570, 2, self.batch)
        self.label = {}
        self.label['high_score'] = Label(x=430, y=415, title='High score',
                batch=self.batch)
        self.label['score'] = Label(x=430, y=391, title='Score',
                batch=self.batch)
        self.label['lives'] = IconLabel(x=430, y=361, title='Lives', img=icon, 
                batch=self.batch)
        self.label['bombs'] = IconLabel(x=430, y=339, title='Bombs', img=icon, 
                batch=self.batch)
        self.high_score = 0
        self.score = 0
        self.lives = 3
        self.bombs = 3

    @property
    def high_score(self):
        return self._high_score

    @high_score.setter
    def high_score(self, value):
        self._high_score = value
        self.label['high_score'].number = self._high_score

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.label['score'].number = self._score

    @property
    def lives(self):
        return self._lives + 1

    @lives.setter
    def lives(self, value):
        self._lives = value - 1
        self.label['lives'].number = self._lives

    @property
    def bombs(self):
        return self._bombs

    @bombs.setter
    def bombs(self, value):
        self._bombs = value
        self.label['bombs'].number = self._bombs

    def on_draw(self):
        self.draw()

    def update(self, dt):
        self.fps.update(dt)

    def draw(self):
        self.bg.blit(0, 0)
        self.batch.draw()
