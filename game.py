#!/usr/bin/env python2

from __future__ import division

import math

import pyglet
from pyglet.window import key

import resources
from constants import *

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

    shots
    BulletGroup containing player shots

    """

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)
        self.focus = 0
        self.speed_multiplier = 10
        self.focus_multiplier = .5
        self.shooting = 0
        self.shot_rate = 30
        self.shot_state = 0
        self.shots = BulletGroup()
        self.keys = key.KeyStateHandler()

    def speed(self):
        if self.focus:
            return self.speed_multiplier * self.focus_multiplier
        else:
            return self.speed_multiplier

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = 1
        elif symbol == key.Z:
            self.shooting = 1

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = 0
        elif symbol == key.Z:
            self.shooting = 0

    def on_draw(self):
        self.shots.draw()
        self.draw()

    def update(self, dt):
        # movement
        x = 0
        if self.keys[key.LEFT]:
            x = -1
        if self.keys[key.RIGHT]:
            x += 1
        y = 0
        if self.keys[key.DOWN]:
            y = -1
        if self.keys[key.UP]:
            y += 1
        if not x == y == 0:
            v = Vector(x, y).get_unit_vector()
            self.x += self.speed() * v.x
            self.y += self.speed() * v.y
        # bullet generation
        if self.shooting:
            self.shot_state += dt
            period = 1 / self.shot_rate  # period of shot
            i = 0
            while self.shot_state > period:
                shot = Bullet(img=resources.shot_image, x=self.x, y=self.y)
                v = shot.direction * shot.speed
                v = v * i
                shot.x += v.x
                shot.y += v.y
                self.shots.add(shot)
                self.shot_state -= period
                i += period
        # bullet movement
        self.shots.update(dt)


class Enemy(Sprite):

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)


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
