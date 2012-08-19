#!/usr/bin/env python3

from game.bullet.reimu import ReimuShot
from game import resources
from game.player import BasePlayer

class Reimu(BasePlayer):

    def __init__(self, keys=None):
        super().__init__(img=resources.player['reimu']['player'],
                hbimg=resources.player['reimu']['hitbox'], keys=keys)

    def update_fire(self, dt):
        period = 1 / self.shot_rate  # period of shot
        i = 0
        while self.shot_state > period:
            shot = ReimuShot(x=self.x - 10, y=self.bottom)
            shot.update(i)
            self.shots.add(shot)
            shot = ReimuShot(x=self.x + 10, y=self.bottom)
            shot.update(i)
            self.shots.add(shot)
            self.shot_state -= period
            i += period
