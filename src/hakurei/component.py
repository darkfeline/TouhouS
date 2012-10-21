#!/usr/bin/env python3

from pyglet import sprite, text
from gensokyo import ces
from gensokyo import locator


class GraphicsObject(Position):

    def __init__(self, type, group, *args, **kwargs):
        self.sprite = type(*args, **kwargs)
        self.group = group
        locator.view.add_sprite(self.sprite, group)

    @property
    def x(self):
        return self.sprite.x

    @x.setter
    def x(self, value):
        self.sprite.x = value

    @property
    def y(self):
        return self.sprite.y

    @y.setter
    def y(self, value):
        self.sprite.y = value

    def delete(self):
        self.sprite.delete()


class Sprite(GraphicsObject):

    def __init__(self, *args, **kwargs):
        super().__init__(sprite.Sprite, *args, **kwargs)


class Label(GraphicsObject):

    def __init__(self, *args, **kwargs):
        super().__init__(text.Label, *args, **kwargs)

    @property
    def label(self):
        return self.sprite


class GameData(ces.Component):

    def __init__(self, high_score=0, score=0, lives=3, bombs=3):
        self.high_score = high_score
        self.score = score
        self.lives = lives
        self.bombs = bombs


class Presence(ces.Component):

    """Used for garbage collecting out-of-bounds entities"""

    def __init__(self, rect):
        self.rect = rect


class EnemyAI(ces.Component):

    def __init__(self, script):
        self.script = script
        self.step = 0
        self.sleep = 0


class Life(ces.Component):

    def __init__(self, life):
        self.life = life
