#!/usr/bin/env python3

import pyglet
from pyglet.window import key
from pyglet import gl

from gensokyo.game import Game
from gensokyo import resources
from gensokyo.constants import WIDTH, HEIGHT, FPS

def main():
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
    pyglet.clock.schedule_interval(update, 1./FPS)
    pyglet.clock.set_fps_limit(FPS)

    pyglet.app.run()

if __name__ == "__main__":
    main()
