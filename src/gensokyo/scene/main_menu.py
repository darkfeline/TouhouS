import logging
import sys

from pyglet.window import key

from gensokyo import locator
from gensokyo import state
from gensokyo import globals
from gensokyo.state import Transition
from gensokyo.state import game
from gensokyo.ces import graphics

logger = logging.getLogger(__name__)


class MenuScene(state.Scene):

    def __init__(self):

        logger.info("Initializing MenuScene...")
        super().__init__()

        self.graphics = MenuGraphics()
        self.input = MenuInput()

        logger.debug("Making Label...")
        self.title = graphics.Label(
            'text', x=20, y=globals.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))

    def enter(self, root):
        locator.window.push_handlers(self.input)
        locator.graphics.push(self.graphics)

    def exit(self, root):
        locator.window.remove_handlers(self.input)
        locator.graphics.pop(self.graphics)

    def delete(self):
        super().delete()


class MenuGraphics(graphics.GraphicsLevel):

    map = ('bg', 'text')


class MenuInput:

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            sys.exit()
        else:
            locator.state_tree.dispatch_event(
                "to_transition", Transition(game.GameScene(), False))
