#!/usr/bin/env python3

import pyglet
from pyglet.window import key
from pyglet import gl
from gensokyo.scene import Scene, SceneStack
from gensokyo.controller import Controller

from hakurei.globals import WIDTH, HEIGHT, FPS
from hakurei.model import MenuModel
from hakurei.view import MenuView
from hakurei import resources

def main():
    window = pyglet.window.Window(WIDTH, HEIGHT)
    window.set_caption('TouhouS')
    window.set_icon(resources.icon16, resources.icon32)
    window.clear()

    # Transparency
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    # Scene Stack
    stack = SceneStack(window)

    # init stuff
    stack.push(Scene(Controller(), MenuModel(), MenuView()))

    pyglet.clock.schedule_interval(stack.update, 1./FPS)
    pyglet.clock.set_fps_limit(FPS)

    pyglet.app.run()

if __name__ == "__main__":
    main()
