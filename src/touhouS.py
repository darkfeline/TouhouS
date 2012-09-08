#!/usr/bin/env python3

import pyglet
from pyglet.window.key import KeyStateHandler
from pyglet import gl
from gensokyo import locator
from gensokyo.graphics import RenderingService

from hakurei.globals import WIDTH, HEIGHT, FPS
from hakurei import resources

def main():
    # window
    window = pyglet.window.Window(WIDTH, HEIGHT)
    window.set_caption('TouhouS')
    window.set_icon(resources.icon16, resources.icon32)
    locator.window = window

    # Transparency
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # key_state
    keys = KeyStateHandler()
    window.push_handlers(keys)
    locator.key_state = keys

    # graphics
    rendering = RenderingService()
    locator.rendering = rendering

    pyglet.clock.schedule_interval(stack.update, 1./FPS)
    pyglet.clock.set_fps_limit(FPS)

    pyglet.app.run()

if __name__ == "__main__":
    main()
