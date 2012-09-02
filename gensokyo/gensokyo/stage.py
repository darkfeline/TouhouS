#!/usr/bin/env python3

from gensokyo.enemy import EnemyGroup
from gensokyo.bullet import BulletGroup

class Stage:

    def __init__(self):
        self.bullets = BulletGroup()
        self.enemies = EnemyGroup(self.bullets)
        self.player = None  # reference only

    def update(self, dt):
        self.enemies.update(dt)
        self.bullets.update(dt)
