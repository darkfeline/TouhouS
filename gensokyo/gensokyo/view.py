#!/usr/bin/env python3

import pyglet
from pyglet.graphics import OrderedGroup
from pyglet.text import Label

from gensokyo import constants

class View:

    _map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
            'enemy_bullet', 'ui', 'ui_element')

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.groups = dict(zip(self.__class__._map,
            [OrderedGroup(i) for i in range(len(self.__class__._map))]))
        self.labels = pyglet.graphics.Batch()

    def on_draw(self):
        constants.WINDOW.clear()
        self.batch.draw()
        self.labels.draw()

    def on_add_sprite(self, sprite, group):
        if isinstance(sprite, Label):
            sprite.batch = self.labels
            return
        sprite.group = self.groups[group]
        sprite.batch = self.batch
