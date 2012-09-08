#!/usr/bin/env python3

import pyglet

from gensokyo.object import Object, Group
from gensokyo.primitives import Vector

from hakurei.object.bullet import BulletGroup
from hakurei.object import bullet
from hakurei import resources

class EnemyGroup(Group):

    def __init__(self, bullets=None):
        super().__init__()
        self.bullets = bullets

    @property
    def enemies(self):
        return list(self.objects)

    @enemies.setter
    def enemies(self, value):
        self.objects = set(value)

    def add(self, enemy):
        super().add(enemy)
        if enemy.bullets is not self.bullets:
            enemy.bullets = self.bullets


class Enemy(Object):

    sprite_group = 'enemy'

    def __init__(self, x, y, hb=None):
        super().__init__(x, y, hb)
        self.dest = Vector(x, y)
        self.speed = 0
        self.max_speed = 300
        self.accel = 100
        self.life = 200
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

    def hit(self, dmg):
        self.life -= dmg
        if self.life < 0:
            self.die()

    def die(self):
        pass

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


class GenericEnemy(Enemy):

    sprite_img = resources.enemy['generic']

    def __init__(self, x, y):
        super().__init__(x, y)
        self.hb = self.rect
        self.max_speed = 300
        self.accel = 100
        self.life = 200

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = bullet.RoundBullet(self.x, self.y, vector=v)
        self.bullets.add(b)
