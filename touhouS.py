#!/usr/bin/env python2

from __future__ import division

import pyglet
from pyglet.window import key
from pyglet import gl

import resources
import game

FPS = 1/60.
HEIGHT = 600
WIDTH = 800

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_caption('TouhouS')
window.set_icon(resources.icon1, resources.icon2)

keys = key.KeyStateHandler()
window.push_handlers(keys)

# Transparency
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

# Log events
window.push_handlers(pyglet.window.event.WindowEventLogger())

# Batches/Groups
shots = []
shots_batch = pyglet.graphics.Batch()

fps_display = pyglet.clock.ClockDisplay()
player = game.Player(img=resources.player_image, x=50, y=50)

player_lives = 3

window.push_handlers()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.LSHIFT:
        player.focus = 1
    elif symbol == key.Z:
        player.shooting = 1

@window.event
def on_key_release(symbol, modifiers):
    if symbol == key.LSHIFT:
        player.focus = 0
    elif symbol == key.Z:
        player.shooting = 0

@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    shots_batch.draw()
    player.draw()

def update(dt):
    # player movement
    global player
    global keys
    x = 0
    if keys[key.LEFT]:
        x = -1
    if keys[key.RIGHT]:
        x += 1
    y = 0
    if keys[key.DOWN]:
        y = -1
    if keys[key.UP]:
        y += 1
    if not x == y == 0:
        v = game.Vector(x, y).get_unit_vector()
        player.x += player.speed() * v.x
        player.y += player.speed() * v.y

    # bullet movement
    global shots
    global shots_batch
    temp = []
    for shot in shots:
        v = shot.direction * shot.speed
        shot.x += v.x
        shot.y += v.y
        # bullet deletion
        if shot.x < 0 or shot.x > WIDTH or shot.y < 0 or shot.y > HEIGHT:
            shot.delete()
        else:
            temp.append(shot)
    shots = temp

    # bullet generation
    if player.shooting:
        player.shot_state += dt
        period = 1 / player.shot_rate  # period of shot
        i = 0
        while player.shot_state > period:
            shot = game.Bullet(img=resources.shot_image, x=player.x,
                    y=player.y, batch=shots_batch)
            v = shot.direction * shot.speed
            v = v * i
            shot.x += v.x
            shot.y += v.y
            shots.append(shot)
            player.shot_state -= period
            i += period

pyglet.clock.schedule_interval(update, FPS)

if __name__ == "__main__":
    pyglet.app.run()
