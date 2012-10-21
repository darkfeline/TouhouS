#!/usr/bin/env python3

from gensokyo import ces


class EnemyAI(ces.Component):

    def __init__(self, script):
        self.script = script
        self.step = 0
        self.sleep = 0


class Life(ces.Component):

    def __init__(self, life):
        self.life = life
