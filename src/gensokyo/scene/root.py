from gensokyo import state
from gensokyo.scene import main_menu
from gensokyo.scene import game


class RootTree(state.StateTree):

    valid_states = (main_menu.MenuScene, game.GameScene)
