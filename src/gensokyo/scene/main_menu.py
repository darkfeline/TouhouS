import logging

from pyglet.window import key

from gensokyo import state
from gensokyo import sprite
from gensokyo import gvars
from gensokyo.sprite import SpriteDrawer

logger = logging.getLogger(__name__)


class MenuScene(state.State):

    def __init__(self, rootenv):

        logger.info("Initializing MenuScene...")
        super().__init__(rootenv)
        self.drawer = MenuDrawer()
        self.input = MenuInput(self.rootenv.state)

        logger.debug("Making Label...")
        self.title = sprite.Label(
            'text', x=20, y=gvars.HEIGHT - 30, text="Welcome to TouhouS",
            color=(255, 255, 255, 255))

    def enter(self):
        logger.info("Entering MenuScene...")
        self.rootenv.window.push_handlers(self.input)
        self.rootenv.drawers.add(self.drawer)

    def exit(self):
        logger.info("Exiting MenuScene...")
        self.rootenv.window.remove_handlers(self.input)
        self.rootenv.drawers.remove(self.drawer)


class MenuDrawer(SpriteDrawer):

    layers = ('bg', 'text')


class MenuInput:

    def __init__(self, statem):
        self.statem = statem

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            logger.info('Exiting menu')
            self.statem.event('exit')
        elif symbol == key.SPACE:
            logger.info('Entering game')
            self.statem.event('game')
