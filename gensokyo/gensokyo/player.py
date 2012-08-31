#!/usr/bin/env python3

from pyglet.window import key

from gensokyo.bullet import BulletGroup
from gensokyo.sprite import CollidingSprite
from gensokyo.constants import GAME_AREA
from gensokyo.primitives import Vector

class Player(CollidingSprite):

    _die_invuln = 3

    def __init__(self, img, x=GAME_AREA.width//2+GAME_AREA.left,
            y=GAME_AREA.bottom+40, hbimg=None, hb=None, keys=None, **kwargs):
        super().__init__(img, x, y, **kwargs)
        self.focus = 0
        self.speed_multiplier = 500
        self.focus_multiplier = 0.5
        self.shooting = 0
        self.shot_rate = 20
        self.shot_state = 0
        self.bullets = BulletGroup()
        self.keys = keys
        self.hbimg = hbimg
        self.hb = hb
        self.invuln = 0

    @property
    def x(self):
        return super().x

    @x.setter
    def x(self, value):
        super(Player, self.__class__).x.fset(self, value)
        self.hbimg.x = value

    @property
    def y(self):
        return super().y

    @y.setter
    def y(self, value):
        super(Player, self.__class__).y.fset(self, value)
        self.hbimg.y = value

    @property
    def center(self):
        return (self.x, self.y)

    @center.setter
    def center(self, value):
        self.x, self.y = value

    @property
    def speed(self):
        if self.focus:
            return self.speed_multiplier * self.focus_multiplier
        else:
            return self.speed_multiplier

    def die(self):
        if self.invuln > 0:
            return 1
        else:
            self.invuln += Player._die_invuln
            return 0

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
        self.bullets.draw()
        self.draw()
        if self.focus:
            self.hbimg.blit(self.x, self.y)

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
            # bound movement
            if self.right > GAME_AREA.right:
                self.right = GAME_AREA.right
            elif self.left < GAME_AREA.left:
                self.left = GAME_AREA.left
            if self.bottom < GAME_AREA.bottom:
                self.bottom = GAME_AREA.bottom
            elif self.top > GAME_AREA.top:
                self.top = GAME_AREA.top
        # invuln
        if self.invuln > 0:
            self.invuln -= dt
        # bullet generation
        if self.shooting:
            self.shot_state += dt
            self.update_fire(dt)
        # bullet movement
        self.bullets.update(dt)

    def update_fire(self, dt):
        pass
