#!/usr/bin/env python3

import pyglet
import pygame

class Sprite(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
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
