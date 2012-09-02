#!/usr/bin/env python3

import pyglet

from gensokyo.object import Object, Group
from gensokyo.constants import GAME_AREA
from gensokyo.primitives import Vector

class BulletGroup(Group):

    @property
    def bullets(self):
        return list(self.objects)

    @bullets.setter
    def bullets(self, value):
        self.objects = set(value)

    def delete(self, bullet):
        self.remove(bullet)
        bullet.delete()

    def update(self, dt):
        super().update(dt)
        temp = set()
        for b in self.bullets:
            r = b.rect
            if (r.bottom > GAME_AREA.top or r.top < GAME_AREA.bottom or
                    r.left > GAME_AREA.right or r.right < GAME_AREA.left):
                b.delete()
            else:
                temp.add(b)
        self.bullets = temp


class Bullet(Object):

    sprite_group = 'enemy_bullet'

    def __init__(self, x, y, hb=None, speed=500, vector=Vector(0, 1)):
        super().__init__(x, y, hb)
        self.speed = speed
        self.vector = vector
        self.dmg = 20

    @property
    def vector(self):
        return self._vector

    @vector.setter
    def vector(self, value):
        self._vector = value.get_unit_vector()

    def update(self, dt):
        self.x += self.speed * self.vector.x * dt
        self.y += self.speed * self.vector.y * dt
