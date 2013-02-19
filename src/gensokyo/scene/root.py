from gensokyo import state
from gensokyo.scene import main_menu
from gensokyo.scene import game


class RootTree(state.StateNode):

    valid_states = {'menu': main_menu.MenuScene, 'game': game.GameScene}
