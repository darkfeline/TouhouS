#!/usr/bin/env python2

from __future__ import division

import pyglet
from pyglet.window import key
from pyglet import gl

import resources
import game
from constants import *

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_caption('TouhouS')
window.set_icon(resources.icon1, resources.icon2)

keys = key.KeyStateHandler()
window.push_handlers(keys)

# Transparency
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Log events
#window.push_handlers(pyglet.window.event.WindowEventLogger())

fps_display = pyglet.clock.ClockDisplay()
player = game.Player(img=resources.player_image, x=WIDTH/2, y=50)

player_lives = 3

window.push_handlers(player)
pyglet.clock.schedule_interval(player.update, FPS, keys)

def on_draw():
    window.clear()
    fps_display.draw()
window.push_handlers(on_draw)

if __name__ == "__main__":
    pyglet.app.run()
