"""
The :mod:`gensokyo` engine is heavily event/observer driven.  It
currently uses pyglet's :class:`EventDispatcher` for its event needs.

RootEnv
=======

Simple namedtuple.

Attributes:

window
    pyglet window
key_state
    Key state registered with pyglet window
clock
    pyglet clock

"""

from collections import namedtuple
import logging

import pyglet
from pyglet import gl
from pyglet.window.key import KeyStateHandler

from gensokyo import state
from gensokyo.sprite import DrawerStack, Clearer
from gensokyo.data import scenes
from gensokyo.globals import WIDTH, HEIGHT, FPS
from gensokyo import resources
from gensokyo.master import Master
from gensokyo.clock import Clock

logger = logging.getLogger(__name__)

RootEnv = namedtuple("RootEnv", ['window', 'key_state', 'clock'])


class Engine(Master):

    def __init__(self):

        # RootEnv
        # window
        logger.debug("Initializing window...")
        window = pyglet.window.Window(WIDTH, HEIGHT)
        window.set_caption('TouhouS')
        window.set_icon(resources.icon16, resources.icon32)

        # Transparency
        logger.debug("Setting transparency...")
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # key_state
        logger.debug("Creating KeyState...")
        keys = KeyStateHandler()
        window.push_handlers(keys)
        # clock
        logger.debug("Initializing pyglet clock...")
        clock = pyglet.clock.get_default()
        clock.set_fps_limit(FPS)

        # set rootenv
        Master._rootenv = RootEnv(window, keys, clock)

        # state machine
        logger.debug("Initializing state machine...")
        self._statem = state.StateMachine(self)

        # clock
        logger.debug("Initializing our clock...")
        self._clock = Clock()
        clock.schedule(self.clock.tick)

        # drawstack
        logger.debug("Creating Drawstack...")
        drawer = DrawerStack()
        drawer.add(Clearer(window))
        window.push_handlers(drawer)
        self._drawer = drawer

        self.statem.init(scenes.start)
        logger.info("Finished init.")

    @staticmethod
    def run():
        logger.info("Running...")
        pyglet.app.run()
