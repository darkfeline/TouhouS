#!/usr/bin/env python3

from gensokyo.bullet import BaseBullet
from gensokyo import resources

class RoundBullet(BaseBullet):

    def __init__(self, x, y, vector):
        super().__init__(x, y, img=resources.bullet['round'], speed=300,
                vector=vector)
