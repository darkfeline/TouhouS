#!/usr/bin/env python3

import pyglet
from pyglet.window import key
from pyglet import gl

from game.base import Game
from game import resources
from game.constants import WIDTH, HEIGHT, FPS

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
