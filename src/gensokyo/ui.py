"""
UI module

Contains various CES classes to use in UI
"""

import abc
import weakref

from gensokyo import sprite
from gensokyo import resources


###############################################################################
# Labels
class UILabel(sprite.Label):

    def __init__(self, drawer, *args, **kwargs):
        group = 'ui_element'
        super().__init__(drawer, group, *args, **kwargs)


###############################################################################
# FPS
class FPSDisplay(UILabel):

    def __init__(self, drawer, clock, x, y):
        super().__init__(drawer, x=x, y=y, anchor_x='left', anchor_y='bottom',
                         font_size=10, color=(255, 255, 255, 255))
        clock.push_handlers(self)
        self.clock = weakref.ref(clock)
        self.count = 0

    def on_update(self, dt):
        self.count += dt
        if self.count > 1:
            self.label.text = "{0:.1f}".format(self.clock.get_fps()) + ' fps'
            self.count = 0

    def delete(self):
        self.clock.remove_handlers(self)


###############################################################################
# Counters
class Counter(metaclass=abc.ABCMeta):

    group = 'ui_element'

    @property
    @abc.abstractmethod
    def title(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def value(self):
        raise NotImplementedError


class TextCounter(Counter):

    def __init__(self, drawer, x, y, title, value=0, width=190):

        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                  'color': (0, 0, 0, 255)}

        self._title = sprite.Label(
            drawer, self.group, x=x, y=y, anchor_x='left', **kwargs)
        self.number = sprite.Label(
            drawer, self.group, x=x + width, y=y, anchor_x='right', **kwargs)
        self.drawer = weakref.ref(drawer)

        self.title = title
        self.value = value

    @property
    def title(self):
        return self._title.text

    @title.setter
    def title(self, value):
        self._title.text = value

    @property
    def value(self):
        return self.value.text

    @value.setter
    def value(self, value):
        self.number.text = value


class IconCounter(Counter):

    icon_img = resources.star
    display_max = 8

    def __init__(self, drawer, x, y, title, value=0, width=190):

        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                  'color': (0, 0, 0, 255)}

        self._title = sprite.Label(
            drawer, self.group, x=x, y=y, anchor_x='left', **kwargs)

        self.icons = []
        self.width = width
        self.title = title
        self.value = value
        self.x = x
        self.y = y

    @property
    def title(self):
        return self._title.text

    @title.setter
    def title(self, value):
        self._title.text = value

    @property
    def value(self):
        return len(self.icons)

    @value.setter
    def value(self, value):
        new = min(self.display_max, value)
        # number of icons to add
        delta = new - self.value
        # number of missing icons
        i = self.display_max - self.value
        # add icons
        while delta > 0:
            sprite_ = sprite.Sprite(
                self.sprite_group, self.icon_img, x=self.x + self.width - i *
                self.icon_width, y=self.y)
            self.icons.append(sprite_)
            self.x = self.x
            i -= 1
            delta -= 1
        # remove icons
        while delta < 0:
            self.icons.pop()
            i += 1
            delta += 1

    @property
    def icon_width(self):
        return self.icon_img.width
        self.value = self.value
