#!/usr/bin/env python2

from __future__ import division

from pyglet.window import key

from game import resources
from game import bullet
from game.sprite import Sprite
from game.constants import WIDTH
from game.vector import Vector

class BasePlayer(Sprite):

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)
        self.keys = None

    def update(self, dt): pass


class Player(BasePlayer):

    """
    Player(Sprite)

    focus
    0 is not focused, 1 is focused

    speed_multiplier
    focus_multiplier
    Speed is speed_multiplier * (focus_multiplier if focus else 1).

    shooting
    0 is not shooting, 1 is shooting

    shot_rate
    Shots per second

    shot_state
    Current shot state (FPS and stuff)

    shots
    BulletGroup containing player shots

    keys
    instance KeyStateHandler

    """

    def __init__(self):
        BasePlayer.__init__(self, img=resources.player_image,
                x=WIDTH/2, y=50)
        self.focus = 0
        self.speed_multiplier = 10
        self.focus_multiplier = .5
        self.shooting = 0
        self.shot_rate = 30
        self.shot_state = 0
        self.shots = bullet.BulletGroup()
        self.keys = key.KeyStateHandler()

    def speed(self):
        if self.focus:
            return self.speed_multiplier * self.focus_multiplier
        else:
            return self.speed_multiplier

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = 1
        elif symbol == key.Z:
            self.shooting = 1

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LSHIFT:
            self.focus = 0
        elif symbol == key.Z:
            self.shooting = 0

    def on_draw(self):
        self.shots.draw()
        self.draw()

    def update(self, dt):
        # movement
        x = 0
        if self.keys[key.LEFT]:
            x = -1
        if self.keys[key.RIGHT]:
            x += 1
        y = 0
        if self.keys[key.DOWN]:
            y = -1
        if self.keys[key.UP]:
            y += 1
        if not x == y == 0:
            v = Vector(x, y).get_unit_vector()
            self.x += self.speed() * v.x
            self.y += self.speed() * v.y
        # bullet generation
        if self.shooting:
            self.shot_state += dt
            period = 1 / self.shot_rate  # period of shot
            i = 0
            while self.shot_state > period:
                shot = bullet.PlayerBullet(x=self.x, y=self.y)
                v = shot.direction * shot.speed
                v = v * i
                shot.x += v.x
                shot.y += v.y
                self.shots.add(shot)
                self.shot_state -= period
                i += period
        # bullet movement
        self.shots.update(dt)
