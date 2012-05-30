#!/usr/bin/env python3

from pyglet.window import key

from game import bullet
from game.sprite import Sprite
from game.constants import WIDTH
from game.vector import Vector

class Player(Sprite):

    def __init__(self, x=WIDTH/2, y=300, img=None, *args, **kwargs):
        super().__init__(*args, x=x, y=y, img=img, **kwargs)
        self.focus = 0
        self.speed_multiplier = 500
        self.focus_multiplier = .5
        self.shooting = 0
        self.shot_rate = 70
        self.shot_state = 0
        self.shots = bullet.BulletGroup()
        self.keys = key.KeyStateHandler()

    @property
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
            self.x += self.speed * v.x * dt
            self.y += self.speed * v.y * dt
        # bullet generation
        if self.shooting:
            self.shot_state += dt
            self.update_fire(dt)
        # bullet movement
        self.shots.update(dt)

    def update_fire(self, dt):
        period = 1 / self.shot_rate  # period of shot
        i = 0
        while self.shot_state > period:
            shot = bullet.Bullet(x=self.x, y=self.y)
            shot.update(i)
            self.shots.add(shot)
            self.shot_state -= period
            i += period
