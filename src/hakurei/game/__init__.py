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


class BoundState:

    def __init__(self):
        self.state = 0


class Wrapper(Entity):

    def __init__(self, component):
        self.add(component)


class GameArea(Entity):

    def __init__(self):
        hb = component.Hitbox(globals.GAME_AREA)
        self.add(hb)


class GameBounds(Entity):

    def __init__(self):
        buffer = 100
        # left bound
        rect = Rect(0, 0, buffer, globals.GAME_AREA.height)
        rect.right = globals.GAME_AREA.left
        hb = component.Hitbox(rect.copy())
        self.add(hb)
        # right bound
        rect.left = globals.GAME_AREA.right
        hb = component.Hitbox(rect.copy())
        self.add(hb)
        # top bound
        rect = Rect(0, 0, globals.GAME_AREA.width, buffer)
        rect.bottom = globals.GAME_AREA.top
        hb = component.Hitbox(rect.copy())
        # bottom bound
        rect = Rect(0, 0, globals.GAME_AREA.width, buffer)
        rect.top = globals.GAME_AREA.bottom
        hb = component.Hitbox(rect.copy())
        self.add(hb)
