import abc
import logging

from pyglet.event import EVENT_HANDLED

from gensokyo import locator

"""
Defines event observer/listener superclasses.  Subclass to implement
functionality.

Observer subclasses define the ``channels`` attribute for which channels it
needs to listen to.  Refer to gensokyo.event for details about channels.

Make sure to properly delete afterward.

This module also defines blockers that block events from propagating to lower
handlers.  Simply instantiating them is fine.  Make sure to hold onto a
reference so you can properly delete them.  Generally this will be done at the
Scene level.

"""

logger = logging.getLogger(__name__)


class Observer(metaclass=abc.ABCMeta):

    """
    Set the channels to listen to.

    """

    channels = set()

    @classmethod
    def expand_channels(cls):
        l = set()
        for class_ in cls.__mro__:
            if issubclass(class_, Observer):
                l |= class_.channels
        return l

    def __init__(self, *args, **kwargs):
        logger.debug("Instantiating Observer {}".format(self))
        logger.debug("Channels: {}".format(self.expand_channels()))
        for chan in self.expand_channels():
            locator.broadcast[chan].push_handlers(self)

    def delete(self):
        for chan in self.expand_channels():
            locator.broadcast[chan].remove_handlers(self)


class Drawing(Observer, metaclass=abc.ABCMeta):

    channels = set(['window'])

    def on_draw(self):
        pass


class DrawBlocker(Drawing):

    def on_draw(self):
        return EVENT_HANDLED


class Input(Observer, metaclass=abc.ABCMeta):

    channels = set(['window'])

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass


class InputBlocker(Input):

    def on_key_press(self, symbol, modifiers):
        return EVENT_HANDLED

    def on_key_release(self, symbol, modifiers):
        return EVENT_HANDLED


class Updating(Observer, metaclass=abc.ABCMeta):

    channels = set(['clock'])

    def on_update(self, dt):
        pass


class UpdateBlocker(Updating):

    def on_update(self, dt):
        return EVENT_HANDLED
