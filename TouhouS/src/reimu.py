#!/usr/bin/env python3

from gensokyo.player import Player
from gensokyo.bullet import Bullet
import resources

class ReimuShot(Bullet):

    def __init__(self, x, y):
        super().__init__(resources.player['reimu']['shot'], x, y)
        self.speed = 1500


class Reimu(Player):

    def __init__(self, keys=None):
        super().__init__(img=resources.player['reimu']['player'],
                hbimg=resources.player['reimu']['hitbox'], keys=keys)
        self.speed_multiplier = 500
        self.focus_multiplier = .5
        self.shot_rate = 20

    def update_fire(self, dt):
        period = 1 / self.shot_rate  # period of shot
        i = 0
        while self.shot_state > period:
            shot = ReimuShot(x=self.x - 10, y=self.bottom)
            shot.update(i)
            self.bullets.add(shot)
            shot = ReimuShot(x=self.x + 10, y=self.bottom)
            shot.update(i)
            self.bullets.add(shot)
            self.shot_state -= period
            i += period
