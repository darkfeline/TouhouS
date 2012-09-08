#!/usr/bin/env python3

from gensokyo import view

class GameView(view.View):

    _map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
            'enemy_bullet', 'ui', 'ui_element')


class MenuView(view.View):

    _map = ('bg', 'text')


