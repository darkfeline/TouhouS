#!/usr/bin/env python3

import pyglet
from pyglet.window import key
from pyglet import gl
from gensokyo.globals import WIDTH, HEIGHT, FPS
from gensokyo import globals
from gensokyo.view import View

from model import Model
import resources

def main():
    window = pyglet.window.Window(WIDTH, HEIGHT)
    globals.WINDOW = window
    window.set_caption('TouhouS')
    window.set_icon(resources.icon16, resources.icon32)
    window.clear()

    # Transparency
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # Logger
    #window.push_handlers(pyglet.window.event.WindowEventLogger())
    # keys
    keys = key.KeyStateHandler()
    window.push_handlers(keys)
    globals.KEYS = keys
    # view
    view = View()
    window.push_handlers(view)
    globals.VIEW = view
    # model
    model = Model()
    window.push_handlers(model)

    def update(dt):
        model.update(dt)
    pyglet.clock.schedule_interval(update, 1./FPS)
    pyglet.clock.set_fps_limit(FPS)

    pyglet.app.run()

if __name__ == "__main__":
    main()
