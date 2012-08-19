#!/usr/bin/env python3

import pyglet

from game.sprite import Sprite
from game.constants import GAME_AREA
from game.primitives import Vector

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
            b.update(dt)
            if (b.bottom > GAME_AREA.top or b.top < GAME_AREA.bottom or b.left
                    > GAME_AREA.right or b.right < GAME_AREA.left):
                b.delete()
            else:
                temp.append(b)
        self.bullets = temp


class BaseBullet(Sprite):

    def __init__(self, x, y, speed=2000, vector=Vector(0, 1), img=None, *args,
            **kwargs):
        super().__init__(*args, x=x, y=y, img=img, **kwargs)
        self.speed = speed
        self._vector = vector.get_unit_vector()

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        self._vector = value.get_unit_vector()

    def update(self, dt):
        self.x += self.speed * self.vector.x * dt
        self.y += self.speed * self.vector.y * dt
