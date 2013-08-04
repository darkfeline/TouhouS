from gensokyo.data.scenes.main_menu import MenuScene
from gensokyo.data.scenes.game import GameScene

__all__ = ['start', 'graph']

start = MenuScene
graph = {
    MenuScene: {
        'exit': None,
        'game': GameScene,
    },
    GameScene: {
        'quit': MenuScene,
    },
}
