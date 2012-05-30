#!/usr/bin/env python3

from __future__ import division

import math

from game.exceptions import NoAngleException

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
