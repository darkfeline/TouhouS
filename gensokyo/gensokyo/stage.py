#!/usr/bin/env python3

from gensokyo.enemy import EnemyGroup

class Stage:

    def __init__(self, player):
        self.enemies = EnemyGroup()
        self.player = player

    def on_draw(self):
        self.enemies.draw()

    def update(self, dt):
        self.enemies.update(dt)
