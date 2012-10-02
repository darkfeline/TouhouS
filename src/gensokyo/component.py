#!/usr/bin/env python3

"""
This module contains the components provided by gensokyo.

In a component/system design, components hold only data.  Systems operate on
entites which own components, and thus all logic are in systems.

"""

import abc

from pyglet import sprite
from pyglet import text

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


class GraphicsObject(Position):

    __metaclass__ = abc.ABCMeta
    type = None

    def __init__(self, group, *args, **kwargs):
        sprite = self.type(*args, **kwargs)
        self.sprite = sprite
        self.group = group
        locator.view.add_sprite(sprite, group)

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


class Sprite(GraphicsObject):

    type = sprite.Sprite


class Label(GraphicsObject):

    type = text.Label


class Velocity:

    """
    Velocity Physics component.  It contains a list whose index is the degree
    of the differential, i.e. 0 is velocity, 1 is acceleration, etc., and value
    is the corresponding Vector.

    .. attribute: vectors
        list of Vectors

    """

    def __init__(self):
        self.vectors = []
