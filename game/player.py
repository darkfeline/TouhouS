#!/usr/bin/env python3

from pyglet.window import key

from game import bullet
from game import resources
from game.sprite import Sprite
from game.constants import GAME_AREA
from game.primitives import Vector

class Player(Sprite):

    def __init__(self, x=GAME_AREA.width/2+GAME_AREA.left, y=GAME_AREA.top+40,
            img=None, hbimg=resources.hitbox_image, *args, **kwargs):
        super().__init__(*args, x=x, y=y, img=img, **kwargs)
        self.focus = 0
        self.speed_multiplier = 500
        self.focus_multiplier = .5
        self.shooting = 0
        self.shot_rate = 50
        self.shot_state = 0
        self.shots = bullet.BulletGroup()
        self.keys = key.KeyStateHandler()
        self.hitbox = Sprite(img=hbimg)

    @property
    def x(self):
        return super().x

    @x.setter
    def x(self, value):
        super(Player, self.__class__).x.fset(self, value)
        self.hitbox.x = value

    @property
    def y(self):
        return super().y

    @y.setter
    def y(self, value):
        super(Player, self.__class__).y.fset(self, value)
        self.hitbox.y = value

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
        if self.focus:
            self.hitbox.draw()

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
            if self.bottom > GAME_AREA.bottom:
                self.bottom = GAME_AREA.bottom
            elif self.top < GAME_AREA.top:
                self.top = GAME_AREA.top
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


class PlayerA(Player):

    def __init__(self):
        super().__init__(img=resources.player_image)

    def update_fire(self, dt):
        period = 1 / self.shot_rate  # period of shot
        i = 0
        while self.shot_state > period:
            shot = bullet.PlayerBullet(x=self.x, y=self.y)
            shot.update(i)
            self.shots.add(shot)
            self.shot_state -= period
            i += period
