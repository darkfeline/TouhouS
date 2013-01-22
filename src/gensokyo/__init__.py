"""
The :mod:`gensokyo` engine is heavily event/observer driven.  It currently uses
pyglet's :class:`EventDispatcher` for its event needs.

.. autoclass:: RootEnv(window, clock, state_tree, key_state)
.. autoclass:: Engine

"""

from collections import namedtuple
import logging

import pyglet
from pyglet import gl
from pyglet.window.key import KeyStateHandler

from gensokyo import state
from gensokyo.clock import Clock
from gensokyo.scene import root
from gensokyo.globals import WIDTH, HEIGHT, FPS
from gensokyo import resources

logger = logging.getLogger(__name__)

RootEnv = namedtuple("RootEnv", ['window', 'clock', 'state_tree', 'key_state'])


class Engine:

    def __init__(self):

        # window
        logger.debug("Initializing window...")
        window = pyglet.window.Window(WIDTH, HEIGHT)
        window.set_caption('TouhouS')
        window.set_icon(resources.icon16, resources.icon32)

        # Transparency
        logger.debug("Setting transparency...")
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # State tree
        logger.debug("Creating state tree...")
        state_tree = state.StateMachine()

        # key_state
        logger.debug("Creating KeyState...")
        keys = KeyStateHandler()
        window.push_handlers(keys)

        # clock
        logger.debug("Initializing clock...")
        clock = Clock()
        pyglet.clock.set_fps_limit(FPS)
        pyglet.clock.schedule(clock.tick)

        # initialize state tree
        logger.debug("init state tree...")
        state_tree.init(
            root.RootTree(), RootEnv(window, clock, state_tree, keys))

        logger.info("Finished init.")

    @staticmethod
    def run():
        logger.info("Running...")
        pyglet.app.run()
