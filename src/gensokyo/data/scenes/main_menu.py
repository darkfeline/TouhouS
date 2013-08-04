import logging

from gensokyo import state
from gensokyo import sprite
from gensokyo import gvars
from gensokyo import menu
from gensokyo.data import stages

logger = logging.getLogger(__name__)


class MenuScene(state.State, menu.Menu):

    def __init__(self, master):
        logger.info("Initializing MenuScene...")
        super().__init__(master, 50, gvars.HEIGHT-100)
        logger.debug("Making Label...")
        self.title = sprite.Label(
            self.drawer, 'menu', x=20, y=gvars.HEIGHT-30,
            text="Welcome to TouhouS", color=(255, 255, 255, 255))
        self.init(MainPane)

    def enter(self):
        logger.info("Entering MenuScene...")
        self.master.drawer.add(self.drawer)

    def exit(self):
        logger.info("Exiting MenuScene...")
        self.master.drawer.remove(self.drawer)

    def hook_exit(self):
        self.event('exit')
        self.master.event('exit')
        self.master.event('hook_exit')

    def hook_start(self, *args):
        self.event('exit')
        self.master.event('game', *args)


class MainPane(menu.MenuPane):

    keys = ('Start', 'Exit')
    map = {
        'Start': 'stage_select',
        'Exit': 'hook_exit'
    }


class StageSelectPane(menu.MenuPane):

    keys = ('Stage One', 'Back')
    map = {
        'Stage One': ('hook_start', stages.stage_one.StageOne),
        'Back': 'back'
    }

MainPane.transitions = {
    'exit': None,
    'stage_select': StageSelectPane
}

StageSelectPane.transitions = {
    'back': MainPane,
    'exit': None
}
