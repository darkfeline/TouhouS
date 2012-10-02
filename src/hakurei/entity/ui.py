#!/usr/bin/env python3

import pyglet
from pyglet.text import Label
from pyglet.sprite import Sprite
from gensokyo import locator
from gensokyo.entity import Entity
from gensokyo import component

from hakurei import resources


class UILabel(Entity):

    sprite_group = 'ui_element'

    def __init__(self, *args, **kwargs):
        super.__init__()
        self.add(Label(self.sprite_group, *args, **kwargs))


class FPSDisplay(UILabel):

    def __init__(self, x, y):
        super.__init__(x=x, y=y, anchor_x='left', anchor_y='bottom',
                font_size=10, color=(255, 255, 255, 255))


class TextCounter(Counter):

    def __init__(self, x, y, title, value=0, width=190):

        super().__init__()

        self._title = Label(anchor_x='left', anchor_y='bottom', font_size=10,
                color=(0, 0, 0, 255))
        self.add_sprite(self._title, self.sprite_group)

        self._number = Label(anchor_x='right', anchor_y='bottom', font_size=10,
                color=(0, 0, 0, 255))
        self.add_sprite(self._number, self.sprite_group)

        self.width = width
        self.x = x
        self.y = y
        self.title = title
        self.value = value

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
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._number.text = str(value)


class IconCounter(Counter):

    icon_img = resources.star
    sprite_group = 'ui_element'

    def __init__(self, x, y, title, value=0, width=190):

        super().__init__()

        self._title = Label(anchor_x='left', anchor_y='bottom',
                font_size=10, color=(0, 0, 0, 255))
        self.add_sprite(self._title, self.sprite_group)

        self._value = 0
        self._display_max = 0

        self.width = width
        self.icons = []
        self.title = title
        self.display_max = 8
        self.value = value
        self.x = x
        self.y = y

    @property
    def icon_width(self):
        return self.icon_img.width

    @property
    def display_max(self):
        return self._display_max

    @display_max.setter
    def display_max(self, value):
        self._display_max = value
        self.value = self.value

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
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        new = min(self.display_max, value)
        delta = new - self.value
        self._value = value
        while delta > 0:
            sprite = Sprite(self.icon_img, y=self.y)
            self.icons.append(sprite)
            self.add_sprite(sprite, self.sprite_group)
            self.x = self.x
            delta -= 1
        while delta < 0:
            sprite = self.icons.pop()
            sprite.delete()
            delta += 1


class UI(SpriteWrapper):

    bg_img = resources.ui_image
    _counters = {'high_score': (TextCounter, 430, 415, 'High score'),
        'score': (TextCounter, 430, 391, 'Score'),
        'lives': (IconCounter, 430, 361, 'Lives'),
        'bombs': (IconCounter, 430, 339, 'Bombs')}
    sprite_group = 'ui'

    def __init__(self):

        super().__init__()

        self.fps = FPSDisplay(570, 2)
        self.label = {}
        for k in self._counters.keys():
            t = self._counters[k]
            self.label[k] = t[0](t[1], t[2], t[3])
        self.bg = Sprite(self.bg_img)
        self.add_sprite(self.bg, self.sprite_group)

    def update(self, dt):
        self.fps.update(dt)

for k in UI._counters.keys():
    def get(self, k=k):
        return getattr(self, '_' + k)
    def set(self, value, k=k):
        setattr(self, '_' + k, value)
        self.label[k].value = value
    setattr(UI, k, property(get, set))
del set
del get
