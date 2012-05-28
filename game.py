#!/usr/bin/env python2

from __future__ import division

from math import sqrt

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
        return sqrt(self.x ** 2 + self.y ** 2)

class Player(Sprite):

    """
    Player(Sprite)

    Attributes:

    move_state = [0, 0]

    First int is x movement, second is y.  x = +1 is right, -1 is left, y = +1
    is up, -1 is down.

    focus = 0

    0 is not focused, 1 is focused

    speed_multiplier
    focus_multiplier

    Speed is speed_multiplier * (focus_multiplier if focus else 1).  Velocity
    is along self.move_state vector.

    """

    _x = 1/sqrt(2)
    _UNIT_VECTORS = {
        -1:{
             -1:Vector(-_x, -_x),
             0:Vector(-1, 0),
             1:Vector(-_x, _x)
         },
         0:{
             -1:Vector(0, -_x),
             0:Vector(0, 0),
             1:Vector(0, _x)
         }, 
         1:{
             -1:Vector(_x, -_x),
             0:Vector(1, 0),
             1:Vector(_x, _x)
         } 
    }
    del _x

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)
        self.move_state = [0, 0]
        self.focus = 0
        self.speed_multiplier = 10
        self.focus_multiplier = .5

    def speed(self):
        if self.focus:
            return self.speed_multiplier * self.focus_multiplier
        else:
            return self.speed_multiplier

    def vector(self):
        x = self.move_state
        return Player._UNIT_VECTORS[x[0]][x[1]]
