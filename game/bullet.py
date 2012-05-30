#!/usr/bin/env python3

import pyglet

from game.sprite import Sprite
from game.constants import WIDTH, HEIGHT
from game import resources
from game.vector import Vector

class BaseBullet(Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class BaseBulletGroup:

    def add(self, bullet): pass

    def draw(self): pass

    def update(self, dt): pass


class BulletGroup(BaseBulletGroup):

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


class PlayerBullet(BaseBullet):

    def __init__(self, x, y):
        super().__init__(img=resources.shot_image, x=x, y=y)
        self.speed = 30
        self.direction = Vector(0, 1)
