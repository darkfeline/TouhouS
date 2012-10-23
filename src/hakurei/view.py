from gensokyo.view import View


class GameView(View):

    _map = ('player', 'player_bullet', 'player_hb', 'enemy', 'item',
            'enemy_bullet', 'ui', 'ui_element')


class MenuView(View):

    _map = ('bg', 'text')


class GameView(View):

    _map = ('fg', 'ui')
