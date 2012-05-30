#!/usr/bin/env python3

from game.sprite import Sprite
from game import resources
from game.bullet import BulletGroup, Bullet

class EnemyGroup:

    def __init__(self):
        self.enemies = []
        self.batch = pyglet.graphics.Batch()
        self.bullets = BulletGroup()

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

    def __init__(self, x, y):
        super().__init__(img=resources.enemy_image, x=x, y=y)
