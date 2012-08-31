#!/usr/bin/env python3

from gensokyo.enemy import Enemy
from gensokyo.primitives import Vector, Circle
from gensokyo.bullet import Bullet
import resources

class RoundBullet(Bullet):

    def __init__(self, x, y, vector):
        super().__init__(resources.bullet['round'], x, y, speed=300,
                vector=vector)
        self.hb = Circle(x, y, 10)


class GenericEnemy(Enemy):

    def __init__(self, x, y):
        super().__init__(resources.enemy['generic'], x, y)
        self.hb = self.rect
        self.max_speed = 300
        self.accel = 100
        self.life = 200

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = RoundBullet(self.x, self.y, vector=v)
        self.bullets.add(b)
