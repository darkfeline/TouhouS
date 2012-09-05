#!/usr/bin/env python3

from gensokyo.model.enemy import EnemyGroup
from gensokyo.model.bullet import BulletGroup
from gensokyo.model.object import SpriteWrapper

class Stage(SpriteWrapper):

    def __init__(self):
        super().__init__()
        self.bullets = BulletGroup()
        self.enemies = EnemyGroup(self.bullets)
        self.player = None  # reference only

    def update(self, dt):
        self.enemies.update(dt)
        self.bullets.update(dt)
        self.add_sprites(self.enemies)
        self.add_sprites(self.bullets)
