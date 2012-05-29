#!/usr/bin/env python2

from __future__ import division

import math
from abc import ABCMeta, abstractmethod, abstractproperty

import pyglet

from constants import *

class Sprite(pyglet.sprite.Sprite): pass


class Vector(tuple):

    __slots__ = ()

    def __new__(cls, x=0, y=0):
        return tuple.__new__(cls, (x, y))

    @property
    def x(self):
        return tuple.__getitem__(self, 0)

    @property
    def y(self):
        return tuple.__getitem__(self, 1)

    @property
    def length(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    @property
    def angle(self):
        if self.x == 0:
            if self.y > 0:
                return math.pi / 2
            elif self.y < 0:
                return math.pi * 3 / 2
            else:
                raise NoAngleException()
        else:
            return math.fmod(math.atan2(self.y, self.x) + 2 * math.pi,
                    2 * math.pi)

    def get_unit_vector(self):
        t = self.angle
        return Vector(math.cos(t), math.sin(t))

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise NotImplemented
        return Vector(self.x * other, self.y * other)


class NoAngleException(Exception): pass


class AbstractPlayer(Sprite):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)

    @abstractproperty
    def keys(self): pass

    @abstractmethod
    def update(self, dt): pass


class AbstractEnemy(Sprite):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)

    @abstractmethod
    def update(self, dt): pass


class AbstractBullet(Sprite):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)


class BulletGroup:

    def __init__(self):
        self.bullets = []
        self.batch = pyglet.graphics.Batch()

    def add(self, bullet):
        self.bullets.append(bullet)
        bullet.batch = self.batch

    def draw(self):
        self.batch.draw()

    def update(self, dt):
        temp = []
        for b in self.bullets:
            v = b.direction * b.speed
            b.x += v.x
            b.y += v.y
            if b.x < 0 or b.x > WIDTH or b.y < 0 or b.y > HEIGHT:
                b.delete()
            else:
                temp.append(b)
        self.bullets = temp
