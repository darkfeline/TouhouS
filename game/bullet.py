#!/usr/bin/env python3

import pyglet

from game.sprite import Sprite
from game.constants import WIDTH, HEIGHT
from game.vector import Vector
from game import resources

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
            if b.x < 0 or b.x > WIDTH or b.y < 0 or b.y > HEIGHT:
                b.delete()
            else:
                temp.append(b)
        self.bullets = temp


class Bullet(Sprite):

    def __init__(self, x, y, speed=2000, vector=Vector(0, 1), img=None, *args,
            **kwargs):
        super().__init__(*args, x=x, y=y, img=img, **kwargs)
        self.speed = speed
        self.vector = vector.get_unit_vector()

    def update(self, dt):
        self.x += self.speed * self.vector.x * dt
        self.y += self.speed * self.vector.y * dt


class PlayerBullet(Bullet):

    def __init__(self, x, y):
        super().__init__(x, y, img=resources.shot_image)


class EnemyBullet(Bullet):

    def __init__(self, x, y, vector):
        super().__init__(x, y, img=resources.bullet_image, speed=300,
                vector=vector)
