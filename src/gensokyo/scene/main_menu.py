import logging

from gensokyo import locator
from gensokyo import scene
from gensokyo import globals
from gensokyo.scene import game
from gensokyo.ces import graphics
from gensokyo.ces import observer

logger = logging.getLogger(__name__)


class MenuScene(scene.Scene):

    def __init__(self):
        super().__init__()
        g = MenuGraphics()
        self.sm.add(g)
        locator.broadcast.open('graphics', g)
        self.sm.add(MenuInput())

    def init(self):
        logger.info("Initializing MenuScene...")
        logger.debug("Making Label...")
        self.title = graphics.Label(
            'text', x=20, y=globals.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))
        logger.info("Finished initializing MenuScene.")

    def start(self):
        logger.info("Adding GameScene...")
        locator.scene_stack.push(game.GameScene())


class MenuGraphics(graphics.Graphics):

    _map = ('bg', 'text')


class MenuInput(observer.Input):

    def on_key_press(self, symbol, modifiers):
        locator.scene.start()
