#!/usr/bin/env python3

import pyglet

from gensokyo.sprite import Sprite, Group
from gensokyo.primitives import Vector
from gensokyo.bullet import BulletGroup

class EnemyGroup(Group):

    def __init__(self):
        super().__init__()
        self.bullets = BulletGroup()

    @property
    def enemies(self):
        return self.sprites

    @enemies.setter
    def enemies(self, value):
        self.sprites = value

    def add(self, enemy):
        super().add(enemy)
        if enemy.bullets is not self.bullets:
            enemy.bullets = self.bullets

    def draw(self):
        super().draw()

    def update(self, dt):
        super().update(dt)


class Enemy(Sprite):

    def __init__(self, img, x=0, y=0, **kwargs):
        super().__init__(img, x, y, **kwargs)
        self.dest = Vector(x, y)
        self.speed = 0
        self.max_speed = 300
        self.accel = 100
        self.bullets = None

    @property
    def accel_dist(self):
        return self.max_speed - self.speed

    @property
    def decel_dist(self):
        return self.speed

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, value):
        self._dest = value
        self._vector = value - Vector(self.x, self.y)
        self._vector = self._vector.get_unit_vector()

    @property
    def vector(self):
        return self._vector

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = bullet.Bullet(self.x, self.y, vector=v)
        self.bullets.add(b)

    def update(self, dt):
        # movement
        diff = self.dest - Vector(self.x, self.y)
        if diff != Vector(0, 0):
            # acceleration/deceleration
            if diff.length <= self.decel_dist:
                self.speed -= self.accel * dt
            if self.speed < self.max_speed:
                self.speed += self.accel * dt
            # movement
            self.x += self.speed * self.vector.x * dt
            self.y += self.speed * self.vector.y * dt
