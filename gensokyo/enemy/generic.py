#!/usr/bin/env python3

from gensokyo.enemy import BaseEnemy
from gensokyo.primitives import Vector
from gensokyo.bullet.round import RoundBullet
from gensokyo import resources

class GenericEnemy(BaseEnemy):

    def __init__(self, x, y):
        super().__init__(x, y, img=resources.enemy['generic'])

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = RoundBullet(self.x, self.y, vector=v)
        self.bullets.add(b)
