#!/usr/bin/env python3

from gensokyo.object import SpriteAdder
from gensokyo.player import Player
from gensokyo.stage import Stage
from gensokyo.ui import UI
from gensokyo.globals import DEF_PLAYER_XY as XY

class Model(SpriteAdder):

    ui_class = None
    player_class = None
    stage_class = None

    def __init__(self):

        cls = self.__class__

        self.ui = cls.ui_class()
        self.player = cls.player_class(XY[0], XY[1])
        self.stage = cls.stage_class()
        self.stage.player = self.player

        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.bombs = 3

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.ui.score = value

    @property
    def high_score(self):
        return self._high_score

    @high_score.setter
    def high_score(self, value):
        self._high_score = value
        self.ui.high_score = value

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        self.ui.lives = value - 1

    @property
    def bombs(self):
        return self._bombs

    @bombs.setter
    def bombs(self, value):
        self._bombs = value
        self.ui.bombs = value

    def on_key_press(self, symbol, modifiers):
        self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol, modifiers):
        self.player.on_key_release(symbol, modifiers)

    def update(self, dt):

        self.ui.update(dt)
        self.player.update(dt)
        self.stage.update(dt)

        # player + enemy bullet
        x = self.player.collide(self.stage.bullets)
        if x:
            for b in x:
                self.stage.bullets.delete(b)
            if not self.player.die() and self.lives > 1:
                self.lives -= 1
            else:
                # game over
                pass

        # enemy + player bullet
        x = self.stage.enemies.collide(self.player.bullets)
        for e in x.keys():
            for b in x[e]:
                e.hit(b.dmg)
                self.player.bullets.delete(b)
            if e.life < 0:
                self.stage.enemies.delete(e)

        self.add_sprites(self.ui)
        self.add_sprites(self.player)
        self.add_sprites(self.stage)
