from gensokyo.scene import main_menu
from gensokyo.scene import game

main_menu.MenuScene.transitions = {'exit': None, 'game': game.GameScene}
game.GameScene.transitions = {'quit': main_menu.MenuScene}
