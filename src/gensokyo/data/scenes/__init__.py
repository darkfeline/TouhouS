from gensokyo.data.scenes import main_menu
from gensokyo.data.scenes import game

__all__ = ['start', 'main_menu', 'game']

start = main_menu.MenuScene
main_menu.MenuScene.transitions = {'exit': None, 'game': game.GameScene}
game.GameScene.transitions = {'quit': main_menu.MenuScene}
