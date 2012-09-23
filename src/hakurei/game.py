#!/usr/bin/env python3

from pyglet.text import Label
from pyglet.event import EVENT_HANDLED
from gensokyo.primitives import Vector
from gensokyo.game import Scene

from hakurei.object.player import Reimu
from hakurei.object.stage import StageOne
from hakurei.object.ui import UI
from hakurei.globals import DEF_PLAYER_XY as XY
from hakurei.globals import HEIGHT, WIDTH

class ShootingScene(Scene):

    ui_class = UI
    player_class = Reimu
    stage_class = StageOne

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

    def update(self, dt):

        super().update(dt)

        self.ui.update(dt)
        self.player.update(dt)
        self.stage.update(dt)

        # player + enemy bullet
        x = self.player.collide(self.stage.bullets)
        if x:
            for b in x:
                self.stage.bullets.delete(b)
            if not self.player.die():
                if self.lives > 1:
                    self.lives -= 1
                else:
                    return

        # enemy + player bullet
        x = self.stage.enemies.collide(self.player.bullets)
        for e in x.keys():
            for b in x[e]:
                e.hit(b.dmg)
                self.player.bullets.delete(b)
            if e.life < 0:
                self.stage.enemies.delete(e)

        return EVENT_HANDLED


class MenuModel:

    def __init__(self):
        self.title = Label(x=20, y=HEIGHT-30, text="Welcome to TouhouS",
                color=(255, 255, 255, 255))

    def on_attach(self):
            self.add_sprite(self.title, 'text')

    def on_key_press(self, symbol, modifiers):
        scene = Scene(self.master.controller, GameModel(), view.GameView())
        self.master.dispatch_event('on_push_scene', scene)
        self.sprites = set((self.title,))
