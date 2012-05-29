#!/usr/bin/env python2

from __future__ import division

import pyglet
from pyglet.window import key
from pyglet import gl

import resources
import basic
from constants import *

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_caption('TouhouS')
window.set_icon(resources.icon1, resources.icon2)

# Transparency
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

to_update = []

# Logger
#window.push_handlers(pyglet.window.event.WindowEventLogger())
# FPS
fps_display = pyglet.clock.ClockDisplay()
# keys
keys = key.KeyStateHandler()
window.push_handlers(keys)
# player
player = basic.Player()
window.push_handlers(player)
window.push_handlers(player.keys)
to_update.append(player)

player_lives = 3

# Global event handlers
window.push_handlers()

@window.event
def on_draw():
    window.clear()
    fps_display.draw()

# Global update
def update(dt):
    for x in to_update:
        x.update(dt)
pyglet.clock.schedule_interval(update, FPS)

if __name__ == "__main__":
    pyglet.app.run()
