import abc

from pyglet.event import EVENT_HANDLED

from gensokyo import ces
from gensokyo import locator


class Observer:

    __meta__ = abc.ABCMeta

    def delete(self, *args, **kwargs):
        pass


class Input(Observer):

    __meta__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        locator.window.push_handlers(self)

    def delete(self, *args, **kwargs):
        super().delete(self, *args, **kwargs)
        locator.window.remove_handlers(self)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_key_release(self, symbol, modifiers):
        pass


class InputBlocker(ces.System, Input):

    def on_key_press(self, symbol, modifiers):
        return EVENT_HANDLED

    def on_key_release(self, symbol, modifiers):
        return EVENT_HANDLED


class Updating(Observer):

    __meta__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        locator.clock.push_handlers(self)

    def delete(self, *args, **kwargs):
        super().delete(self, *args, **kwargs)
        locator.clock.remove_handlers(self)

    def on_update(self, dt):
        pass


class UpdateBlocker(ces.System, Updating):

    def on_update(self, dt):
        return EVENT_HANDLED
