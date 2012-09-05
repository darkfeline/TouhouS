#!/usr/bin/env python3

import abc

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.graphics import OrderedGroup
from pyglet.text import Label
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup

class AbstractView:

    __metaclass__ = abc.ABCMeta

    @property
    def master(self):
        return self._master

    @master.setter
    def master(self, value):
        self._master = value

    @abc.abstractmethod
    def on_draw(self, sprite, group):
        raise NotImplementedError

    @abc.abstractmethod
    def on_add_sprite(self, sprite, group):
        raise NotImplementedError


class View(AbstractView):

    _map = tuple()

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.groups = dict(zip(self.__class__._map,
            [OrderedGroup(i) for i in range(len(self.__class__._map))]))
        self.master = None
        self.labels = set()

    def on_draw(self):
        self.master.window.clear()
        self.batch.draw()
        for l in self.labels:
            l.draw()
        return EVENT_HANDLED

    def on_add_sprite(self, sprite, group):
        if isinstance(sprite, Label):
            self.add_label(sprite, group)
        else:
            self.add_sprite(sprite, group)
        return EVENT_HANDLED

    def add_label(self, label, group):
        self.labels.add(label)
        #set_label_group(label, self.groups[group])
        #label.batch = self.batch
        #label._own_batch = False

    def add_sprite(self, sprite, group):
        try:
            sprite.group = self.groups[group]
        except AttributeError:  # sprite already deleted
            return
        except KeyError:  # wrong group, probably from previous view
            return
        sprite.batch = self.batch


def set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
            TextLayoutForegroundDecorationGroup(2, label.top_group)
