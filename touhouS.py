#!/usr/bin/env python2

from __future__ import division

import pyglet
from pyglet.window import key
from pyglet import gl

import resources
import game

FPS = 1/60.

window = pyglet.window.Window(800, 600)
window.set_caption('TouhouS')
window.set_icon(resources.icon1, resources.icon2)

keys = key.KeyStateHandler()
window.push_handlers(keys)

# Transparency
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Log events
window.push_handlers(pyglet.window.event.WindowEventLogger())

fps_display = pyglet.clock.ClockDisplay()
player = game.Player(img=resources.player_image, x=50, y=50)

player_lives = 3

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LEFT:
        player.move_state[0] = -1
    elif symbol == key.RIGHT:
        player.move_state[0] = 1
    elif symbol == key.UP:
        player.move_state[1] = 1
    elif symbol == key.DOWN:
        player.move_state[1] = -1
    elif symbol == key.LSHIFT:
        player.focus = 1

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.LEFT or symbol == key.RIGHT:
        player.move_state[0] = 0
    elif symbol == key.UP or symbol == key.DOWN:
        player.move_state[1] = 0
    elif symbol == key.LSHIFT:
        player.focus = 0

@window.event
def on_draw():
    window.clear()
    player.draw()
    fps_display.draw()

def update(dt):
    v = player.vector()
    player.x += player.speed() * v.x
    player.y += player.speed() * v.y

pyglet.clock.schedule_interval(update, FPS)

if __name__ == "__main__":
    pyglet.app.run()
