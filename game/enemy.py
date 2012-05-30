#!/usr/bin/env python3

from game.sprite import Sprite
from game import resources

class BaseEnemy(Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update(self, dt): pass


class Enemy(BaseEnemy):

    def __init__(self, x, y):
        super().__init__(img=resources.enemy_image, x=x, y=y)
