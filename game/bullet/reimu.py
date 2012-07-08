#!/usr/bin/env python3

from game.bullet import BaseBullet
from game import resources

class ReimuShot(BaseBullet):

    def __init__(self, x, y):
        super().__init__(x, y, img=resources.player['reimu']['shot'])
