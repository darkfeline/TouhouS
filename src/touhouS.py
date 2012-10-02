#!/usr/bin/env python3

import pyglet
from pyglet.window.key import KeyStateHandler
from pyglet import gl
from gensokyo import locator
from gensokyo.scene import SceneStack, Scene

from hakurei.globals import WIDTH, HEIGHT, FPS
from hakurei import resources
from hakurei.model import GameModel
from hakurei.view import GameView


def main():
    # window
    window = pyglet.window.Window(WIDTH, HEIGHT)
    window.set_caption('TouhouS')
    window.set_icon(resources.icon16, resources.icon32)
    locator.window = window

    # Transparency
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # game
    scene_stack = SceneStack()
    window.push_handlers(scene_stack)
    locator.scene_stack = scene_stack

    # key_state
    keys = KeyStateHandler()
    window.push_handlers(keys)
    locator.key_state = keys

    # clock
    pyglet.clock.schedule_interval(locator.scene_stack.update, 1 / FPS)
    pyglet.clock.set_fps_limit(FPS)

    locator.game.push(Scene(GameModel(), GameView()))

    pyglet.app.run()

if __name__ == "__main__":
    main()
