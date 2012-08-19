#!/usr/bin/env python3

from gensokyo.player.reimu import Reimu as Player
from gensokyo.stages.generic import Stage
from gensokyo.ui import UI

class Game:

    def __init__(self, keys):
        self.to_update = []

        # UI
        self.ui = UI()
        self.to_update.append(self.ui)
        # player
        self.player = Player(keys=keys)
        self.to_update.append(self.player)
        # stage
        self.stage = Stage(self.player)
        self.to_update.append(self.stage)

    @property
    def player_lives(self):
        return self.ui.player_lives

    @player_lives.setter
    def player_lives(self, value):
        self.ui.player_lives = value

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
        for x in self.to_update:
            x.update(dt)

    def on_draw(self, *args):
        self.player.on_draw(*args)
        self.stage.on_draw(*args)
        self.ui.on_draw(*args)

    def on_key_press(self, *args):
        self.player.on_key_press(*args)

    def on_key_release(self, *args):
        self.player.on_key_release(*args)

