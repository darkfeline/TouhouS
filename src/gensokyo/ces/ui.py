"""
UI module

Contains various CES classes to use in UI

"""

import abc

from pyglet import clock
from gensokyo import ces
from gensokyo.ces import graphics
from gensokyo import resources


###############################################################################
# Labels
###############################################################################
class UILabel(ces.Entity):

    sprite_group = 'ui_element'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.add(graphics.Label(self.sprite_group, *args, **kwargs))


###############################################################################
# FPS
###############################################################################
class FPSDisplay(UILabel):

    def __init__(self, x, y):
        super().__init__(x=x, y=y, anchor_x='left', anchor_y='bottom',
                       font_size=10, color=(255, 255, 255, 255))


class FPSSystem(ces.System):

    def __init__(self, env):
        super().__init__(env)
        self.count = 0

    def on_update(self, dt):
        self.count += dt
        if self.count > 1:
            entity = self.env.tm.get_tag('fps_display')
            for l in entity.get(graphics.Label):
                l.label.text = "{0:.1f}".format(clock.get_fps()) + ' fps'
            self.count = 0


###############################################################################
# Counters
###############################################################################
class Counter(ces.Entity, metaclass=abc.ABCMeta):

    sprite_group = 'ui_element'

    @property
    @abc.abstractmethod
    def title(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def value(self):
        raise NotImplementedError


class TextCounter(Counter):

    def __init__(self, x, y, title, value=0, width=190):

        super().__init__()
        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                  'color': (0, 0, 0, 255)}

        self._title = graphics.Label(self.sprite_group, x=x, y=y,
                                    anchor_x='left', **kwargs)
        self.add(self._title)
        self.number = graphics.Label(self.sprite_group, x=x + width, y=y,
                                     anchor_x='right', **kwargs)
        self.add(self.number)

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

    def __init__(self, x, y, title, value=0, width=190):

        super().__init__()
        kwargs = {'anchor_y': "bottom", 'font_size': 10,
                  'color': (0, 0, 0, 255)}

        self._title = graphics.Label(
            self.sprite_group, x=x, y=y, anchor_x='left', **kwargs)
        self.add(self._title)

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
            sprite = graphics.Sprite(
                self.sprite_group, self.icon_img, x=self.x + self.width - i *
                self.icon_width, y=self.y)
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
