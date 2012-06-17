#!/usr/bin/env python3

from game.enemy.base import EnemyGroup

class BaseStage:

    def __init__(self, player):
        self.enemies = EnemyGroup()
        self.player = player

    def on_draw(self):
        self.enemies.draw()

    def update(self, dt):
        self.enemies.update(dt)
