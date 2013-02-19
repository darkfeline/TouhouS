import logging

from pyglet.window import key

from gensokyo import state
from gensokyo import gvars
from gensokyo.scene import game
from gensokyo import graphics

logger = logging.getLogger(__name__)


class MenuScene(state.State):

    transitions = {'exit': None, 'game': game.GameScene}

    def __init__(self):

        logger.info("Initializing MenuScene...")

        self.graphics = MenuGraphics()

        logger.debug("Making Label...")
        self.title = graphics.Label(
            'text', x=20, y=gvars.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))

    def enter(self, rootenv):
        logger.info("Entering MenuScene...")
        self.input = MenuInput(rootenv.state)
        rootenv.window.push_handlers(self.input)
        rootenv.graphics.push(self.graphics)

    def exit(self, rootenv):
        logger.info("Exiting MenuScene...")
        rootenv.window.remove_handlers(self.input)
        del self.input
        rootenv.graphics.pop()


class MenuGraphics(graphics.GraphicsLevel):

    map = ('bg', 'text')


class MenuInput:

    def __init__(self, statem):
        self.statem = statem

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.statem.event('exit')
        elif symbol == key.SPACE:
            self.statem.event('game')
