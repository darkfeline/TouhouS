#!/usr/bin/env python3

import pyglet

from game.sprite import Sprite
from game.vector import Vector
from game import bullet
from game import resources

class EnemyGroup:

    def __init__(self):
        self.enemies = []
        self.batch = pyglet.graphics.Batch()
        self.bullets = bullet.BulletGroup()

    def add(self, enemy):
        self.enemies.append(enemy)
        enemy.batch = self.batch
        enemy.bullets = self.bullets

    def draw(self):
        self.batch.draw()
        self.bullets.draw()

    def update(self, dt):
        for enemy in self.enemies:
            enemy.update(dt)
        self.bullets.update(dt)


class Enemy(Sprite):

    def __init__(self, x, y, img=None, *args, **kwargs):
        super().__init__(*args, x=x, y=y, img=img, **kwargs)
        self.dest = Vector(x, y)
        self.speed = 0
        self.max_speed = 250
        self.accel = 500
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


class EnemyA(Enemy):

    def __init__(self, x, y):
        super().__init__(x, y, img=resources.enemy_image)

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = bullet.EnemyBullet(self.x, self.y, vector=v)
        self.bullets.add(b)
