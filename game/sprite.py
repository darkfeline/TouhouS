#!/usr/bin/env python2

import pyglet
import pygame

class Sprite(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        pyglet.sprite.Sprite.__init__(self, *args, **kwargs)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self._x, self._y

    @property
    def x(self):
        return pyglet.sprite.Sprite.x.fget(self)

    @x.setter
    def x(self, value):
        pyglet.sprite.Sprite.x.fset(self, value)
        self.rect.centerx = value

    @property
    def y(self):
        return pyglet.sprite.Sprite.y.fget(self)

    @y.setter
    def y(self, value):
        pyglet.sprite.Sprite.y.fset(self, value)
        self.rect.centery = value
