#!/usr/bin/env python3

from gensokyo.player import Player
from gensokyo.stage import Stage

class Game:

    def __init__(self, keys, ui, player=Player, stage=Stage):
        self.ui = ui
        self.player = player(keys=keys)
        self.stage = stage(self.player)

    @property
    def lives(self):
        return self.ui.lives

    @lives.setter
    def lives(self, value):
        self.ui.lives = value

    @property
    def score(self):
        return self.ui.score

    @score.setter
    def score(self, value):
        self.ui.score = value

    @property
    def high_score(self):
        return self.ui.high_score

    @high_score.setter
    def high_score(self, value):
        self.ui.high_score = value

    def update(self, dt):
        self.ui.update(dt)
        self.player.update(dt)
        self.stage.update(dt)

        # player + enemy bullet
        x = self.player.collide_group(self.stage.bullets)
        if x:
            self.player.die()
            self.stage.bullets.delete(x[0])
            if self.lives > 0:
                self.lives -= 1
            else:
                pass

        # enemy + player bullet
        x = self.stage.enemies.collide_group(self.player.bullets)
        for e in x.keys():
            for b in x[e]:
                e.hit(b.dmg)
                self.player.bullets.delete(b)
            if e.life < 0:
                self.stage.enemies.delete(e)

    def on_draw(self):
        self.player.on_draw()
        self.stage.on_draw()
        self.ui.on_draw()

    def on_key_press(self, *args):
        self.player.on_key_press(*args)

    def on_key_release(self, *args):
        self.player.on_key_release(*args)
