import logging

from gensokyo import locator
from gensokyo import scene
from gensokyo.scene import game
from gensokyo.ces import graphics

logger = logging.getLogger(__name__)


class MenuScene(scene.Scene):

    def init(self):
        logger.info("Initializing MenuScene...")
        super().__init__()
        logger.debug("Making Label...")
        self.title = graphics.Label(
            x=20, y=globals.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))
        logger.info("Finished initializing MenuScene.")

    def on_key_press(self, symbol, modifiers):
        logger.info("Adding GameScene...")
        locator.scene_stack.push(game.GameScene())


class MenuGraphics(graphics.Graphics):

    _map = ('bg', 'text')
