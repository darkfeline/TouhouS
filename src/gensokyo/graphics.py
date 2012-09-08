#!/usr/bin/env python3

import abc

import pyglet
from pyglet.event import EVENT_HANDLED
from pyglet.graphics import OrderedGroup, Batch
from pyglet.text import Label
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup

from gensokyo import locator

class AbstractRenderingService:

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def on_draw(self):
        raise NotImplementedError

    @abc.abstractmethod
    def on_add_sprite(self, sprite, group):
        raise NotImplementedError


class NullRenderingService:

    def on_draw(self):
        return EVENT_HANDLED

    def on_add_sprite(self, sprite, group):
        return EVENT_HANDLED


class RenderingService(AbstractRenderingService):

    def __init__(self):
        self.views = []

    def push(self, view):
        self.views.append(view)

    def pop(self):
        self.views.pop()
        return EVENT_HANDLED

    def on_draw(self):
        locator.window.clear()
        self.views[-1].draw()
        return EVENT_HANDLED

    def add_sprite(self, sprite, group):
        self.views[-1].add_sprite(sprite, group)


class View:

    _map = tuple()

    def __init__(self):
        self.batch = Batch()
        self.groups = dict(zip(self.map, 
            [OrderedGroup(i) for i in range(len(self.map))]))
        self.master = None
        self.labels = set()

    @property
    def map(self):
        return self.__class__._map

    def draw(self):
        self.batch.draw()
        for l in self.labels:
            l.draw()

    def add_sprite(self, sprite, group):
        if isinstance(sprite, Label):
            self._add_label(sprite, group)
        else:
            self._add_sprite(sprite, group)

    def _add_label(self, label, group):
        self.labels.add(label)
        #set_label_group(label, self.groups[group])
        #label.batch = self.batch
        #label._own_batch = False

    def _add_sprite(self, sprite, group):
        try:
            sprite.group = self.groups[group]
        except AttributeError:  # sprite already deleted
            return
        sprite.batch = self.batch


def set_label_group(label, group):
    label.top_group = TextLayoutGroup(group)
    label.background_group = OrderedGroup(0, label.top_group)
    label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
    label.foreground_decoration_group = \
            TextLayoutForegroundDecorationGroup(2, label.top_group)
