from gensokyo import state
from gensokyo.scene import main_menu
from gensokyo.scene import game


class RootTree(state.StateTree):

    map = (main_menu.MenuScene, game.GameScene)
