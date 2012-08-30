#!/usr/bin/env python3

from gensokyo.enemy import EnemyGroup
from gensokyo.bullet import BulletGroup

class Stage:

    def __init__(self, player):
        self.bullets = BulletGroup()
        self.enemies = EnemyGroup(self.bullets)
        self.player = player

    def on_draw(self):
        self.enemies.draw()
        self.bullets.draw()

    def update(self, dt):
        self.enemies.update(dt)
        self.bullets.update(dt)
