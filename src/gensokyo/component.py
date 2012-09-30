#!/usr/bin/env python3

import abc

from pyglet.event import EventDispatcher
from pyglet import sprite

from gensokyo.primitives import Rect, Circle
from gensokyo import locator


class Position:

    """
    Abstract Interface for components who have a position, i.e. x, y
    coordinates that need to be updated by physics

    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def x(self):
        raise NotImplementedError

    @abc.abstractproperty
    def y(self):
        raise NotImplementedError


class Hitbox(Position):

    def __init__(self, hb):
        self.hb = hb

    @property
    def x(self):
        if isinstance(self.hb, Circle):
            return self.hb.x
        elif isinstance(self.hb, Rect):
            return self.hb.centerx

    @x.setter
    def x(self, value):
        if isinstance(self.hb, Circle):
            self.hb.x = value
        elif isinstance(self.hb, Rect):
            self.hb.centerx = value

    @property
    def y(self):
        if isinstance(self.hb, Circle):
            return self.hb.y
        elif isinstance(self.hb, Rect):
            return self.hb.centery

    @y.setter
    def y(self, value):
        if isinstance(self.hb, Circle):
            self.hb.y = value
        elif isinstance(self.hb, Rect):
            self.hb.centery = value


class Sprite(Position):

    def __init__(self, group, *args, **kwargs):
        sprite = sprite.Sprite(*args, **kwargs)
        self.sprite = sprite
        self.group = group
        locator.rendering.add_sprite(sprite, group)

    @property
    def x(self):
        return self.sprite.x

    @x.setter
    def x(self, value):
        self.sprite.x = value

    @property
    def y(self):
        return self.sprite.y

    @y.setter
    def y(self, value):
        self.sprite.y = value

    def delete(self):
        self.sprite.delete()


class Velocity:

    def __init__(self):
        self.vectors = []
