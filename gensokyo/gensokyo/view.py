#!/usr/bin/env python3

import pyglet
from pyglet.graphics import OrderedGroup
from pyglet.text import Label
from pyglet.text.layout import TextLayoutGroup, TextLayoutForegroundGroup
from pyglet.text.layout import TextLayoutForegroundDecorationGroup

from gensokyo import globals

class View:

    _map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
            'enemy_bullet', 'ui', 'ui_element')

    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        self.groups = dict(zip(self.__class__._map,
            [OrderedGroup(i) for i in range(len(self.__class__._map))]))

    def on_draw(self):
        globals.WINDOW.clear()
        self.batch.draw()

    def on_add_sprite(self, sprite, group):
        if isinstance(sprite, Label):
            self.set_label_group(sprite, self.groups[group])
        else:
            sprite.group = self.groups[group]
        sprite.batch = self.batch
        if isinstance(sprite, Label):
            sprite._own_batch = False


    def set_label_group(self, label, group):
        label.top_group = TextLayoutGroup(group)
        label.background_group = OrderedGroup(0, label.top_group)
        label.foreground_group = TextLayoutForegroundGroup(1, label.top_group)
        label.foreground_decoration_group = \
                TextLayoutForegroundDecorationGroup(2, label.top_group)
