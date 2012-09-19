#!/usr/bin/env python3

import pyglet
from pyglet.window.key import KeyStateHandler
from pyglet import gl
from gensokyo import locator
from gensokyo.graphics import RenderingService
from gensokyo.game import Game
from gensokyo.collision import CollisionManager

from hakurei.globals import WIDTH, HEIGHT, FPS
from hakurei import resources
from hakurei.game import ShootingScene
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
    game = Game()
    locator.game = game

    # key_state
    keys = KeyStateHandler()
    window.push_handlers(keys)
    locator.key_state = keys

    # graphics
    rendering = RenderingService()
    window.push_handlers(rendering)
    locator.rendering = rendering

    # collision
    collision = CollisionManager()
    locator.collision = collision

    # clock
    pyglet.clock.schedule_interval(locator.game.update, 1./FPS)
    pyglet.clock.set_fps_limit(FPS)

    locator.rendering.push(GameView())
    locator.game.push(ShootingScene())

    pyglet.app.run()

if __name__ == "__main__":
    main()
