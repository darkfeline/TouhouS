#!/usr/bin/env python3

from gensokyo.bullet import BaseBullet
from gensokyo import resources

class ReimuShot(BaseBullet):

    def __init__(self, x, y):
        super().__init__(x, y, img=resources.player['reimu']['shot'])
