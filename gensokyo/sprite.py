#!/usr/bin/env python3

import pyglet

from gensokyo import primitives

class Sprite(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect = primitives.Rect(0, 0, self.width, self.height)
        self.rect.center = self.x, self.y

    @property
    def x(self):
        return super().x

    @x.setter
    def x(self, value):
        super(Sprite, self.__class__).x.fset(self, value)
        self.rect.centerx = value

    @property
    def y(self):
        return super().y

    @y.setter
    def y(self, value):
        super(Sprite, self.__class__).y.fset(self, value)
        self.rect.centery = value

    @property
    def top(self):
        return self.rect.top

    @top.setter
    def top(self, value):
        self.rect.top = value
        self.x, self.y = self.rect.center

    @property
    def left(self):
        return self.rect.left

    @left.setter
    def left(self, value):
        self.rect.left = value
        self.x, self.y = self.rect.center

    @property
    def bottom(self):
        return self.rect.bottom

    @bottom.setter
    def bottom(self, value):
        self.rect.bottom = value
        self.x, self.y = self.rect.center

    @property
    def right(self):
        return self.rect.right

    @right.setter
    def right(self, value):
        self.rect.right = value
        self.x, self.y = self.rect.center

    @property
    def topleft(self):
        return self.rect.topleft

    @topleft.setter
    def topleft(self, value):
        self.rect.topleft = value
        self.x, self.y = self.rect.center

    @property
    def topright(self):
        return self.rect.topright

    @topright.setter
    def topright(self, value):
        self.rect.topright = value
        self.x, self.y = self.rect.center

    @property
    def bottomleft(self):
        return self.rect.bottomleft

    @bottomleft.setter
    def bottomleft(self, value):
        self.rect.bottomleft = value
        self.x, self.y = self.rect.center

    @property
    def bottomright(self):
        return self.rect.bottomright

    @bottomright.setter
    def bottomright(self, value):
        self.rect.bottomright = value
        self.x, self.y = self.rect.center


class CollidingSprite(Sprite):

    def __init__(self, *args, hb=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.hb = hb

    def collide(self, other):
        try:
            return self.hb.collide(other)
        except NotImplementedError as e:
            raise e

class Group:

    def __init__(self):
        self.sprites = set()
        self.batch = pyglet.graphics.Batch()

    @property
    def sprites(self):
        return list(self._sprites)

    @sprites.setter
    def sprites(self, value):
        self._sprites = set(value)

    def add(self, sprite):
        self._sprites.add(sprite)
        if sprite.batch is not self.batch:
            sprite.batch = self.batch

    def __iter__(self):
        return iter(self._sprites)

    def draw(self):
        self.batch.draw()

    def update(self, dt):
        for sprite in self:
            sprite.update(dt)
