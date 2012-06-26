#!/usr/bin/env python3

import pyglet
from pyglet.text import Label

from game import resources
from game.sprite import Sprite

class FPSDisplay(pyglet.clock.ClockDisplay):
    pass


class UILabel:

    def __init__(self, x, y, title, number=0, width=190):
        self._title = Label(anchor_x='left', anchor_y='bottom', font_size=10,
                color=(0, 0, 0, 255))
        self._number = Label(anchor_x='right', anchor_y='bottom', font_size=10,
                color=(0, 0, 0, 255))
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

    def draw(self):
        self._title.draw()
        self._number.draw()


class IconLabel(UILabel):

    def __init__(self, x, y, title, number=0, width=190, img=resources.star):
        self._title = Label(anchor_x='left', anchor_y='bottom',
                font_size=10, color=(0, 0, 0, 255))
        self.title = title
        self.width = width
        self.img = img
        self.icons = ()
        self.display_max = 8
        self.icon_width = self.icons[0].width
        self.number = number
        self.x = x
        self.y = y
        self.batch = pyglet.graphics.Batch()

    @property
    def display_max(self):
        return len(self.icons)

    @display_max.setter
    def display_max(self, value):
        self.icons = tuple([Sprite(img=self.img) for i in range(value)])

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
        i = 0
        for i in range(self.number):
            self.icons[i].batch = self.batch
            if i == self.display_max:
                break
        for i in range(i + 1, self.display_max):
            self.icons[i].batch = None

    def draw(self):
        self._title.draw()
        self.batch.draw()


class UI:

    def __init__(self):
        self.bg = resources.ui_image
        self.fps = FPSDisplay()
        self.label = {}
        self.label['high_score'] = UILabel(x=430, y=415, title='High score')
        self.label['score'] = UILabel(x=430, y=391, title='Score')
        self.label['lives'] = IconLabel(x=430, y=361, title='Lives')
        self.label['bombs'] = IconLabel(x=430, y=339, title='Bombs')
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
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
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
        pass

    def draw(self):
        self.bg.blit(0, 0)
        for k in self.label.keys():
            self.label[k].draw()
        self.fps.draw()
