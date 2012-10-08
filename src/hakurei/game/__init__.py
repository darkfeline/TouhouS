#!/usr/bin/env python3

from gensokyo.entity import Entity
from gensokyo.primitives import Rect
from gensokyo import component

from hakurei import globals


class GameData:

    def __init__(self, high_score=0, score=0, lives=3, bombs=3):
        self.high_score = high_score
        self.score = score
        self.lives = lives
        self.bombs = bombs


class Wrapper(Entity):

    def __init__(self, component):
        self.add(component)


class GameArea(Entity):

    def __init__(self):
        hb = component.Hitbox(globals.GAME_AREA)
        self.add(hb)
