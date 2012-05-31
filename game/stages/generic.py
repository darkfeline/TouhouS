#!/usr/bin/env python3

from game import enemy
from game.constants import GAME_AREA
from game.vector import Vector

class Enemy(enemy.EnemyA):

    def __init__(self, x, y, player):
        super().__init__(x, y)
        self.state = 0
        self.player = player

    def update(self, dt):
        super().update(dt)
        self.state += dt
        while self.state > .5:
            self.fire_at(self.player.center)
            self.state -= .5


class Stage:

    def __init__(self, player):
        self.enemies = enemy.EnemyGroup()
        self.player = player
        self.state = 0
        self.rate = 1

    def on_draw(self):
        self.enemies.draw()

    def update(self, dt):
        self.enemies.update(dt)
        self.state += dt
        while self.state > self.rate:
            e = Enemy(GAME_AREA.right+30, 400, self.player)
            e.dest = Vector(GAME_AREA.left-30, 300)
            self.enemies.add(e)
            self.state -= self.rate
