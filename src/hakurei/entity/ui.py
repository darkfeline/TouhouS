#!/usr/bin/env python3

import abc

from pyglet.text import Label
from gensokyo import component
from gensokyo.entity import Entity
from gensokyo import locator

from hakurei import resources
from hakurei.entity import ui
from hakurei.entity import Wrapper


class UILabel(Entity):

    sprite_group = 'ui_element'

    def __init__(self, *args, **kwargs):
        super.__init__()
        self.add(Label(self.sprite_group, *args, **kwargs))


class FPSDisplay(UILabel):

    def __init__(self, x, y):
        super.__init__(x=x, y=y, anchor_x='left', anchor_y='bottom',
                font_size=10, color=(255, 255, 255, 255))


class Counter(Entity):

    __metaclass__ = abc.ABCMeta
    sprite_group = 'ui_element'

    @abc.abstractmethod
    def set_title(self, value):
        raise NotImplementedError

    @abc.abstractmethod
    def set_value(self, value):
        raise NotImplementedError


class TextCounter(Counter):

    def __init__(self, x, y, title, value=0, width=190):

        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                'color': (0, 0, 0, 255)}

        self.title = component.Label(self.sprite_group, x=x, y=y,
                anchor_x='left', **kwargs)
        self.add(self.title)
        self.number = component.Label(self.sprite_group, x=x + width, y=y,
                anchor_x='right', **kwargs)
        self.add(self.number)

        self.set_title(title)

    def set_title(self, value):
        self.title.text = value

    def set_value(self, value):
        self.number.text = value


class IconCounter(Counter):

    icon_img = resources.star
    display_max = 8

    def __init__(self, x, y, title, value=0, width=190):

        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                'color': (0, 0, 0, 255)}

        self.title = component.Label(x=x, y=y, anchor_x='left', **kwargs)
        self.add(title)

        self.icons = []
        self.width = width
        self.set_title(title)
        self.set_value(value)
        self.x = x
        self.y = y

    @property
    def value(self):
        return len(self.icons)

    def set_title(self, value):
        self.title.text = value

    def set_value(self, value):
        new = min(self.display_max, value)
        # number of icons to add
        delta = new - self.value
        # number of missing icons
        i = self.display_max - self.value
        # add icons
        while delta > 0:
            sprite = component.Sprite(self.sprite_group, self.icon_img,
                    x=self.x + self.width - i * self.icon_width, y=self.y)
            self.icons.append(sprite)
            self.x = self.x
            i -= 1
            delta -= 1
        # remove icons
        while delta < 0:
            sprite = self.icons.pop()
            sprite.delete()
            i += 1
            delta += 1

    @property
    def icon_width(self):
        return self.icon_img.width
        self.value = self.value


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
