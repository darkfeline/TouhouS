#!/usr/bin/env python2

from game.sprite import Sprite
from game import resources

class BaseEnemy(Sprite):

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)

    def update(self, dt): pass


class Enemy(BaseEnemy):

    def __init__(self, x, y):
        BaseEnemy.__init__(self, img=resources.enemy_image, x=x, y=y)
