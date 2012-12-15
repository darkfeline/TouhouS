import logging

from pyglet.window import key

from gensokyo import locator
from gensokyo import state
from gensokyo import scene
from gensokyo import globals
from gensokyo.ces import graphics

logger = logging.getLogger(__name__)


class MenuScene(scene.Scene):

    def __init__(self):

        logger.info("Initializing MenuScene...")
        super().__init__()

        self.graphics = MenuGraphics()
        self.input = MenuInput()

        logger.debug("Making Label...")
        self.title = graphics.Label(
            'text', x=20, y=globals.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))

    def enter(self):
        logger.info("Entering MenuScene...")
        super().enter()
        locator.window.push_handlers(self.input)
        locator.graphics.push(self.graphics)

    def exit(self):
        logger.info("Exiting MenuScene...")
        super().exit()
        locator.window.remove_handlers(self.input)
        locator.graphics.pop()

    def delete(self):
        super().delete()


class MenuGraphics(graphics.GraphicsLevel):

    map = ('bg', 'text')


class MenuInput:

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            locator.state_tree.dispatch_event(
                "on_transition", state.Transition('null', False))
        else:
            locator.state_tree.dispatch_event(
                "on_transition", state.Transition('game', False))
