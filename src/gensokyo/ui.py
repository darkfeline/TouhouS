"""
ui
==

Various UI related things.  These are not part of ECS, are generally
instantiated and managed by top-level, e.g. master/scene/state, which also
manages the ECS world.
"""

import abc
import weakref
import logging

from gensokyo import sprite
from gensokyo import resources

__all__ = ['UILabel', 'FPSDisplay', 'Counter', 'TextCounter', 'IconCounter']
logger = logging.getLogger(__name__)
UI_GROUP = 'ui_element'


###############################################################################
# Labels
class UILabel(sprite.Label):

    def __init__(self, drawer, *args, **kwargs):
        group = UI_GROUP
        super().__init__(drawer, group, *args, **kwargs)


###############################################################################
# FPS
class FPSDisplay(UILabel):

    """
    Display FPS of clock.  clock in the __init__() constructor is a pyglet
    clock.  You'll have to register on_update with a gensokyo Clock
    (EventDispatcher).
    """

    def __init__(self, drawer, x, y, clock):
        super().__init__(drawer, x=x, y=y, anchor_x='left', anchor_y='bottom',
                         font_size=10, color=(255, 255, 255, 255))
        self.count = 0
        self.get_clock = weakref.ref(clock)

    @property
    def clock(self):
        return self.get_clock()

    def on_update(self, dt):
        self.count += dt
        if self.count > 1:
            logger.debug("Updating FPS display")
            self.label.text = "{0:.1f}".format(self.clock.get_fps()) + ' fps'
            self.count = 0


###############################################################################
# Counters
class Counter(metaclass=abc.ABCMeta):

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

        logger.debug(
            'Initializing TextCounter(%r, %r, %r, %r, %r, %r)', drawer, x, y,
            title, value, width)
        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                  'color': (0, 0, 0, 255)}

        self._title = UILabel(
            drawer, x=x, y=y, anchor_x='left', **kwargs)
        self.number = UILabel(
            drawer, x=x + width, y=y, anchor_x='right', **kwargs)

        self.title = title
        self.value = value

    @property
    def title(self):
        return self._title.label.text

    @title.setter
    def title(self, value):
        self._title.label.text = value

    @property
    def value(self):
        return self.number.label.text

    @value.setter
    def value(self, value):
        self.number.label.text = str(value)


class IconCounter(Counter):

    icon_img = resources.star
    display_max = 8

    def __init__(self, drawer, x, y, title, value=0, width=190):

        logger.debug(
            'Initializing IconCounter(%r, %r, %r, %r, %r, %r)', drawer, x, y,
            title, value, width)
        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                  'color': (0, 0, 0, 255)}

        self._title = UILabel(
            drawer, x=x, y=y, anchor_x='left', **kwargs)

        self.x = x
        self.y = y
        self.icons = []
        self.drawer = drawer
        self.width = width
        self.title = title
        self.value = value

    @property
    def title(self):
        return self._title.label.text

    @title.setter
    def title(self, value):
        self._title.label.text = value

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
                self.drawer, UI_GROUP, img=self.icon_img,
                x=self.x + self.width - i * self.icon_width, y=self.y)
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
