#!/usr/bin/env python2

from abc import ABCMeta, abstractmethod

from game.sprite import Sprite
from game import resources

class AbstractEnemy(Sprite):

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        Sprite.__init__(self, *args, **kwargs)

    @abstractmethod
    def update(self, dt): pass


class Enemy(AbstractEnemy):

    def __init__(self, x, y):
        AbstractEnemy.__init__(self, img=resources.enemy_image, x=x, y=y)
