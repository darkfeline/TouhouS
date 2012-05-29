#!/usr/bin/env python2

from abc import ABCMeta, abstractmethod

import pyglet

from game.sprite import Sprite
from game.constants import WIDTH, HEIGHT
from game import resources
from game.vector import Vector

class AbstractBullet(Sprite):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)


class AbstractBulletGroup:

    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, bullet): pass

    @abstractmethod
    def draw(self): pass

    @abstractmethod
    def update(self, dt): pass


class BulletGroup(AbstractBulletGroup):

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


class PlayerBullet(AbstractBullet):

    def __init__(self, x, y):
        AbstractBullet.__init__(self, img=resources.shot_image, x=x, y=y)
        self.speed = 30
        self.direction = Vector(0, 1)
