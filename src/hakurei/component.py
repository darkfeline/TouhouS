#!/usr/bin/env python3

import abc

from pyglet import sprite, text
from gensokyo import ces
from gensokyo import primitives
from gensokyo import locator


class Position(ces.Component):

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
        if isinstance(self.hb, primitives.Circle):
            return self.hb.x
        elif isinstance(self.hb, primitives.Rect):
            return self.hb.centerx

    @x.setter
    def x(self, value):
        if isinstance(self.hb, primitives.Circle):
            self.hb.x = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.centerx = value

    @property
    def y(self):
        if isinstance(self.hb, primitives.Circle):
            return self.hb.y
        elif isinstance(self.hb, primitives.Rect):
            return self.hb.centery

    @y.setter
    def y(self, value):
        if isinstance(self.hb, primitives.Circle):
            self.hb.y = value
        elif isinstance(self.hb, primitives.Rect):
            self.hb.centery = value


class GraphicsObject(Position):

    def __init__(self, type, group, *args, **kwargs):
        self.sprite = type(*args, **kwargs)
        self.group = group
        locator.view.add_sprite(self.sprite, group)

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

    def __init__(self, *args, **kwargs):
        super().__init__(sprite.Sprite, *args, **kwargs)


class Label(GraphicsObject):

    def __init__(self, *args, **kwargs):
        super().__init__(text.Label, *args, **kwargs)

    @property
    def label(self):
        return self.sprite


class Physics(ces.Component):

    """
    Physics component.

    .. attribute: vel
        velocity
    .. attribute: acc
        acceleration

    """

    def __init__(self):
        self.vel = primitives.Vector(0, 0)
        self.acc = primitives.Vector(0, 0)

    @property
    def speed(self):
        return self.vel.length


class GameData(ces.Component):

    def __init__(self, high_score=0, score=0, lives=3, bombs=3):
        self.high_score = high_score
        self.score = score
        self.lives = lives
        self.bombs = bombs


class Presence(ces.Component):

    """Used for garbage collecting out-of-bounds entities"""

    def __init__(self, rect):
        self.rect = rect


class EnemyAI(ces.Component):

    def __init__(self, script):
        self.script = script
        self.step = 0
        self.sleep = 0


class Life(ces.Component):

    def __init__(self, life):
        self.life = life
