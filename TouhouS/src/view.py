#!/usr/bin/env python3

from gensokyo import view

class MenuView(view.View):

    _map = ('bg', 'text')

    def on_draw(self):
        super().on_draw()

    def on_add_sprite(self, sprite, group):
        super().on_add_sprite(sprite, group)
