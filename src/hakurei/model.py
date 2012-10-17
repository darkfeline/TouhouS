#!/usr/bin/env python3

from pyglet.event import EVENT_HANDLED
from gensokyo.model import Model
from gensokyo.scene import Scene
from gensokyo import component
from gensokyo import locator

import hakurei
from hakurei import game
from hakurei.game import ui
from hakurei import view
from hakurei.globals import DEF_PLAYER_XY as XY
from hakurei.globals import HEIGHT


class GameModel(Model):

    player_class = game.player.Reimu
    stage_class = game.stage.StageOne
    ui_image = resources.ui_image

    def init(self):

        # Entities
        # UI image
        bg = entity.Wrapper(component.Sprite('ui', self.ui_image))
        self.em.add(bg)
        # FPS
        fps = ui.FPSDisplay(570, 2)
        self.em.add(fps)
        self.tm.tag('fps_display', fps)

        # Counters
        counters = {
            'high_score': (ui.TextCounter, 430, 415, 'High score'),
            'score': (ui.TextCounter, 430, 391, 'Score'),
            'lives': (ui.IconCounter, 430, 361, 'Lives'),
            'bombs': (ui.IconCounter, 430, 339, 'Bombs')}
        for tag, a in counters.items():
            c, x, y, tit = a
            counter = c(x, y, tit)
            self.em.add(counter)
            self.tm.tag(tag, counter)

        # Data
        data = hakurei.entity.Wrapper(hakurei.component.GameData())
        self.tm.tag('data', data)

        # Systems
        fps = hakurei.system.FPSSystem()
        self.sm.add(fps)
        data = hakurei.system.DataSystem()
        self.sm.add(data)

        # TODO finish this

    def __init__(self):

        self.ui = self.ui_class()
        self.player = self.player_class(XY[0], XY[1])
        self.stage = self.stage_class()
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


class MenuModel(Model):

    def init(self):
        self.title = component.Label(x=20, y=HEIGHT - 30, text="Welcome to
                TouhouS", color=(255, 255, 255, 255))

    def on_key_press(self, symbol, modifiers):
        locator.scene_stack.push(Scene(GameModel(), view.GameView()))
