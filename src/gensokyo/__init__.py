"""
The :mod:`gensokyo` engine is heavily event/observer driven.  It currently uses
pyglet's :class:`EventDispatcher` for its event needs.

"""

from collections import namedtuple
import logging
import functools

import pyglet
from pyglet import gl
from pyglet.window.key import KeyStateHandler

from gensokyo import locator
from gensokyo import state
from gensokyo import clock
from gensokyo.ces.graphics import Graphics
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
        locator.window = window

        window.set_caption('TouhouS')
        window.set_icon(resources.icon16, resources.icon32)

        # Transparency
        logger.debug("Setting transparency...")
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

        # State tree
        logger.debug("Creating state tree...")
        state_tree = root.RootTree()
        locator.state_tree = state_tree

        # key_state
        logger.debug("Creating KeyState...")
        keys = KeyStateHandler()
        window.push_handlers(keys)
        locator.key_state = keys

        # graphics
        graphics = Graphics()
        locator.graphics = graphics
        window.push_handlers(on_draw=functools.partial(
            graphics.dispatch_event, 'on_draw'))

        # clock
        logger.debug("Initializing clock...")
        clock_ = clock.Clock()
        locator.clock = clock_
        pyglet.clock.set_fps_limit(FPS)
        pyglet.clock.schedule(clock_.tick)

        # initial state
        logger.debug("Setting start state...")
        state_tree.dispatch_event(
            'on_transition', state.Transition('menu', False))

        logger.info("Finished init.")

    @staticmethod
    def run():
        logger.info("Running...")
        pyglet.app.run()
