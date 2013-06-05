from gensokyo.data.scenes import main_menu
from gensokyo.data.scenes import game

start = main_menu
main_menu.MenuScene.transitions = {'exit': None, 'game': game.GameScene}
game.GameScene.transitions = {'quit': main_menu.MenuScene}
