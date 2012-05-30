#!/usr/bin/env python3

from game.sprite import Sprite
from game import resources

class Enemy(Sprite):

    def __init__(self, x, y):
        super().__init__(img=resources.enemy_image, x=x, y=y)
