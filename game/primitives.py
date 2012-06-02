#!/usr/bin/env python3

import math

from pygame import Rect

from game.exceptions import NoAngleException

class Vector(tuple):

    __slots__ = ()

    def __new__(cls, x=0, y=0):
        return super().__new__(cls, (x, y))

    @property
    def x(self):
        return super().__getitem__(0)

    @property
    def y(self):
        return super().__getitem__(1)

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
        try:
            t = self.angle
        except NoAngleException:
            return Vector(0, 0)
        return Vector(math.cos(t), math.sin(t))

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if not isinstance(other, Vector):
            raise NotImplemented
        if (self.x, self.y) == (other.x, other.y):
            return True
        else:
            return False

    def __mul__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            raise NotImplemented
        return Vector(self.x * other, self.y * other)
