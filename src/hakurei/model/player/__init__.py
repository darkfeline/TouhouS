#!/usr/bin/env python3

from pyglet.window import key
from pyglet.sprite import Sprite
from gensokyo.object import Object
from gensokyo.primitives import Vector

from hakurei.model.bullet import BulletGroup
from hakurei.globals import GAME_AREA

class Player(Object):

    sprite_img = None
    sprite_group = 'player'
    hb_img = None
    hb_group = 'player_hb'
    _die_invuln = 3

    def __init__(self, x, y, hb=None):
        super().__init__(x, y, hb=hb)
        self._focus = 0
        self.speed_multiplier = 500
        self.focus_multiplier = 0.5
        self.shooting = 0
        self.shot_rate = 20
        self.shot_state = 0
        self.bullets = BulletGroup()
        self.invuln = 0
        self.v = Vector(0, 0)
        self.hbsprite = None

    @property
    def x(self):
        return super().x

    @x.setter
    def x(self, value):
        super(Player, self.__class__).x.fset(self, value)
        if hasattr(self, 'hbsprite') and self.hbsprite is not None:
            self.hbsprite.x = value

    @property
    def y(self):
        return super().y

    @y.setter
    def y(self, value):
        super(Player, self.__class__).y.fset(self, value)
        if hasattr(self, 'hbsprite') and self.hbsprite is not None:
            self.hbsprite.y = value

    @property
    def speed(self):
        if self.focus:
            return self.speed_multiplier * self.focus_multiplier
        else:
            return self.speed_multiplier

    @property
    def focus(self):
        return int(self._focus)

    @focus.setter
    def focus(self, value):
        f = self.focus
        v = bool(value)
        if f != v:
            self._focus = v
            if v:
                cls = self.__class__
                self.hbsprite = Sprite(cls.hb_img, self.x, self.y)
                self.add_sprite(self.hbsprite, cls.hb_group)
            else:
                self.hbsprite.delete()
                self.hbsprite = None

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

    def update(self, dt):
        # movement
        self.x += self.speed * self.v.x * dt
        self.y += self.speed * self.v.y * dt
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
        # bullet update
        self.bullets.update(dt)
        self.add_sprites(self.bullets)

    def update_fire(self, dt):
        pass
