#!/usr/bin/env python2

from __future__ import division

import math

import pyglet
import pygame

class Sprite(pyglet.sprite.Sprite):
    pass


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

class NoAngleException(Exception):
    pass

class Player(Sprite):

    """
    Player(Sprite)

    focus
    0 is not focused, 1 is focused

    speed_multiplier
    focus_multiplier
    Speed is speed_multiplier * (focus_multiplier if focus else 1).

    shooting
    0 is not shooting, 1 is shooting

    shot_rate
    Shots per second

    shot_state
    Current shot state (FPS and stuff)

    """

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)
        self.focus = 0
        self.speed_multiplier = 10
        self.focus_multiplier = .5
        self.shooting = 0
        self.shot_rate = 30
        self.shot_state = 0

    def speed(self):
        if self.focus:
            return self.speed_multiplier * self.focus_multiplier
        else:
            return self.speed_multiplier


class Bullet(Sprite):

    """
    Bullet(Sprite)

    speed
    direction
    Velocity = speed * direction (unit vector)

    """

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)
        self.speed = 30
        self.direction = Vector(0, 1)
