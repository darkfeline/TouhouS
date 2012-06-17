#!/usr/bin/env python3

from game.enemy.base import BaseEnemy
from game.primitives import Vector
from game.bullet.round import RoundBullet
from game import resources

class GenericEnemy(BaseEnemy):

    def __init__(self, x, y):
        super().__init__(x, y, img=resources.enemy['generic'])

    def fire_at(self, dest):
        dest = Vector(dest[0], dest[1])
        v = dest - Vector(self.x, self.y)
        b = RoundBullet(self.x, self.y, vector=v)
        self.bullets.add(b)
