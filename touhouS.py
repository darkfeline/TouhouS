#!/usr/bin/env python3

import pyglet
from pyglet.window import key
from pyglet import gl

from game import resources
from game.constants import WIDTH, HEIGHT, FPS
from game.player import PlayerA as Player
from game.stages.generic import Stage
from game.ui import UI

class Game:

    def __init__(self, keys):
        self.to_update = []

        # UI
        self.ui = UI()
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


if __name__ == "__main__":
    window = pyglet.window.Window(WIDTH, HEIGHT)
    window.set_caption('TouhouS')
    window.set_icon(resources.icon1, resources.icon2)

    # Transparency
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    to_update = []

    # Logger
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    # keys
    keys = key.KeyStateHandler()
    window.push_handlers(keys)
    # game
    game = Game(keys)
    to_update.append(game)
    window.push_handlers(game)

    def on_draw():
        window.clear()
    window.push_handlers(on_draw)

    def update(dt):
        for x in to_update:
            x.update(dt)
    pyglet.clock.schedule_interval(update, FPS)

    pyglet.app.run()
