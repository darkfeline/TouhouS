#!/usr/bin/env python3

import pyglet
from pyglet.window import key
from pyglet import gl

import game.ui
from game import resources
from game.constants import WIDTH, HEIGHT, FPS
from game.player import PlayerA as Player
from game.stages.generic import Stage

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_caption('TouhouS')
window.set_icon(resources.icon1, resources.icon2)

# Transparency
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

to_update = []

# Logger
#window.push_handlers(pyglet.window.event.WindowEventLogger())
# UI
ui = game.ui.UI()
window.push_handlers(ui)
# keys
keys = key.KeyStateHandler()
window.push_handlers(keys)
# player
player = Player()
window.push_handlers(player)
window.push_handlers(player.keys)
to_update.append(player)
# stage
stage = Stage(player)
window.push_handlers(stage)
to_update.append(stage)

player_lives = 3

# Global event handlers
window.push_handlers()
@window.event
def on_draw():
    window.clear()

# Global update
def update(dt):
    for x in to_update:
        x.update(dt)
pyglet.clock.schedule_interval(update, FPS)

if __name__ == "__main__":
    pyglet.app.run()
