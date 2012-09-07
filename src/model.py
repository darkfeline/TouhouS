#!/usr/bin/env python3

from pyglet.window import key
from pyglet.text import Label
from pyglet.event import EVENT_HANDLED
from gensokyo.scene import Scene
from gensokyo.model import Model
from gensokyo.primitives import Vector

from reimu import Reimu
from stage import StageOne
import view
from ui import UI
from globals import DEF_PLAYER_XY as XY
from globals import HEIGHT, WIDTH

class GameModel(Model):

    ui_class = UI
    player_class = Reimu
    stage_class = StageOne

    def __init__(self):

        self.master = None

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
        return EVENT_HANDLED

    def on_key_release(self, symbol, modifiers):
        self.player.on_key_release(symbol, modifiers)
        return EVENT_HANDLED

    def on_update(self, dt):

        # player movement
        x = 0
        if self.master.controller[key.LEFT]:
            x = -1
        if self.master.controller[key.RIGHT]:
            x += 1
        y = 0
        if self.master.controller[key.DOWN]:
            y = -1
        if self.master.controller[key.UP]:
            y += 1
        self.player.v = Vector(x, y).get_unit_vector()

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
                    self.master.dispatch_event('on_pop_scene')
                    return

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

        return EVENT_HANDLED


class MenuModel(Model):

    def __init__(self):
        self.title = Label(x=20, y=HEIGHT-30, text="Welcome to TouhouS",
                color=(255, 255, 255, 255))

    def on_attach(self):
            self.add_sprite(self.title, 'text')

    def on_key_press(self, symbol, modifiers):
        scene = Scene(self.master.controller, GameModel(), view.GameView())
        self.master.dispatch_event('on_push_scene', scene)
        self.sprites = set((self.title,))
